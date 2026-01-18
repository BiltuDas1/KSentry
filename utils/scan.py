from models import GitLeaks
import subprocess
from pydantic import ValidationError
import json


async def gitleaks(raw_data: bytes) -> list[GitLeaks]:
  command = [
    "gitleaks",
    "stdin",
    "--config",
    "gitleaks.toml",
    "--report-format",
    "json",
    "--report-path",
    "-",
    "--no-banner",
  ]

  process = subprocess.Popen(
    command,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
  )

  stdout, _ = process.communicate(input=raw_data.decode())

  if process.returncode != 1:
    return []

  try:
    data = json.loads(stdout)
    result = []
    for d in data:
      result.append(GitLeaks.model_validate(d))
    return result
  except ValidationError:
    return []
