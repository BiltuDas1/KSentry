from core import settings
from models import ScanData, PullRequesPayload
from utils import jwt, scan, comment, run_scan
from models import GitLeaks
import tempfile
import os


async def fetch_remote_config(token: str, repo: str, default_branch: str) -> str | None:
  """
  Fetches gitleaks.toml from the repository's default branch.
  """
  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.raw",
  }

  # Fetch gitleaks.toml from the root of the repo
  url = (
    f"https://api.github.com/repos/{repo}/contents/gitleaks.toml?ref={default_branch}"
  )

  try:
    response = await settings.HTTPX.get(url, headers=headers)
    if response.status_code == 200:
      return response.text
  except Exception as e:
    print(f"Error fetching remote config: {e}")

  return None


async def check_pr():
  result = await settings.REDIS.blpop("queue", timeout=5)  # type:ignore
  if result is None:
    return None

  _, item = result
  return ScanData.fromBase64(item)


def to_comments(data: list[GitLeaks]) -> list[comment.CommentData]:
  comment_body = "Probably a Secret\n> If it is false positive then add `gitleaks:allow` inline comment to this line, and then force push again"
  result = []
  for leaks in data:
    result.append(
      comment.CommentData(path=leaks.File, line=leaks.StartLine, body=comment_body)
    )
  return result


async def scan_code():
  """
  Scan the code
  """
  while (pr_data := await check_pr()) is not None:
    token: str = await jwt.get_installation_token(pr_data.installation_id)

    # Get the commit hash
    pr_details_resp = await settings.HTTPX.get(
      f"https://api.github.com/repos/{pr_data.repo}/pulls/{pr_data.pr_number}",
      headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",  # Force JSON, not Diff
      },
    )
    if pr_details_resp.status_code != 200:
      continue

    commit_hash = pr_details_resp.json()["head"]["sha"]
    await run_scan.in_progress(token, pr_data.repo, commit_hash)

    headers = {
      "Authorization": f"Bearer {token}",
      "Accept": "application/vnd.github.v3.diff",
    }
    resp = await settings.HTTPX.get(
      f"https://api.github.com/repos/{pr_data.repo}/pulls/{pr_data.pr_number}",
      headers=headers,
    )
    if resp.status_code != 200:
      await run_scan.failure(token, pr_data.repo, commit_hash)
      continue

    config_path = "gitleaks.toml"
    temp_config = None
    remote_config_content = await fetch_remote_config(
      token, pr_data.repo, pr_data.default_branch
    )

    if remote_config_content:
      temp_config = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".toml")
      temp_config.write(remote_config_content)
      temp_config.close()  # Close it so gitleaks subprocess can read it
      config_path = temp_config.name
      print(f"Using remote config for {pr_data.repo}", flush=True)

    try:
      result = await scan.gitleaks(resp.content, config_path)
    finally:
      if temp_config:
        os.remove(temp_config.name)

    # If no secret found leave
    if len(result) == 0:
      await run_scan.success(token, pr_data.repo, commit_hash)
      continue

    review = await comment.comment_on(
      token=token,
      repo=pr_data.repo,
      pull_number=pr_data.pr_number,
      commit_id=commit_hash,
      main_message="Secrets found",
      comments=to_comments(result),
    )
    if review.status_code != 200:
      print("Failed", flush=True)
    else:
      print("Success", flush=True)
    await run_scan.error(token, pr_data.repo, commit_hash)


async def request_scan(payload: PullRequesPayload):
  data = ScanData(
    repo=payload.repository.full_name,
    default_branch=payload.repository.default_branch,
    upstream_branch=payload.pull_request.head.label,
    installation_id=payload.installation.id,
    pr_number=payload.number,
  )

  await settings.REDIS.rpush("queue", data.toBase64())  # type:ignore

  try:
    await settings.HTTPX.get(f"{settings.WORKER_URL}/process")
  except Exception as e:
    print(e)
