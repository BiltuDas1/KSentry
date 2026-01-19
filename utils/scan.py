import re
import json
import asyncio
from typing import List
from pydantic import ValidationError
from models import GitLeaks
import tomllib
from typing import List, Pattern


def parse_allowlist(config_path: str) -> List[Pattern]:
  """
  Parses gitleaks.toml using the standard library's tomllib.
  Returns a list of compiled regex patterns to ignore.
  """
  allowlist_patterns = []
  try:
    with open(config_path, "rb") as f:
      data = tomllib.load(f)

    allowlist = data.get("allowlist", {})

    if isinstance(allowlist, list):
      allowlist = allowlist[0] if allowlist else {}

    raw_paths = allowlist.get("paths", [])

    for p in raw_paths:
      try:
        allowlist_patterns.append(re.compile(p))
      except re.error:
        print(f"Invalid regex in allowlist: {p}")

  except FileNotFoundError:
    print(f"Config file not found: {config_path}")
  except tomllib.TOMLDecodeError as e:
    print(f"Error parsing TOML: {e}")

  return allowlist_patterns


async def gitleaks(
  raw_data: bytes, config_path: str = "gitleaks.toml"
) -> List[GitLeaks]:
  """
  Parses a unified diff, scans each hunk, and calculates
  absolute line numbers for GitHub reporting.
  """
  # Decode the incoming diff
  diff_text = raw_data.decode("utf-8", errors="ignore")

  # Split into File Blocks
  # We split by 'diff --git ' but keep the delimiter
  file_chunks = re.split(r"(?=diff --git )", diff_text)

  ignored_patterns = parse_allowlist(config_path)
  final_results = []

  for file_chunk in file_chunks:
    if not file_chunk.strip():
      continue

    # Extract Filename (b/path/to/file)
    filename_match = re.search(r" b/(.*)", file_chunk.splitlines()[0])
    filename = filename_match.group(1) if filename_match else "unknown"

    if any(pattern.search(filename) for pattern in ignored_patterns):
      continue

    # Split the File Block into individual Hunks (@@ blocks)
    # This ensures line math is accurate for PRs with changes in different parts of a file.
    hunks = re.split(r"(?=@@ )", file_chunk)
    # The first part of the split is the file header (diff --git, ---, +++), we skip it
    hunks.pop(0)

    for hunk in hunks:
      # Extract Hunk Start Line (the + number)
      # Format: @@ -1,4 +150,6 @@ -> extracts 150
      hunk_header_match = re.search(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", hunk)
      if not hunk_header_match:
        continue

      hunk_start_line = int(hunk_header_match.group(1))

      # Calculate how many lines are in the hunk header (usually just 1: the @@ line)
      hunk_lines = hunk.splitlines()
      header_height = 0
      for idx, line in enumerate(hunk_lines):
        if line.startswith("@@"):
          header_height = idx + 1
          break

      # Execute Gitleaks via Async Pipe
      command = [
        "gitleaks",
        "detect",
        "--pipe",
        "--config",
        config_path,
        "--report-format",
        "json",
        "--report-path",
        "-",
        "--no-banner",
      ]

      process = await asyncio.create_subprocess_exec(
        *command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
      )

      # Send the hunk to Gitleaks
      stdout, _ = await process.communicate(input=hunk.encode())

      # Gitleaks returns exit code 1 if leaks are found
      if process.returncode == 1:
        try:
          raw_findings = json.loads(stdout)
          for d in raw_findings:
            # --- THE MATH FIX ---
            # relative_offset: How many lines down from the @@ line the leak is
            # We subtract 1 because the line after @@ is index 0 relative to hunk_start
            relative_offset = d["StartLine"] - header_height - 1

            # Apply absolute line numbers
            d["File"] = filename
            d["StartLine"] = hunk_start_line + relative_offset
            d["EndLine"] = hunk_start_line + (d["EndLine"] - header_height - 1)

            final_results.append(GitLeaks.model_validate(d))
        except (json.JSONDecodeError, ValidationError, KeyError):
          continue

  return final_results
