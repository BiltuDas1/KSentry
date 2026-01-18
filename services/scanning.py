from core import settings
from models import ScanData, PullRequesPayload
from utils import jwt, scan, comment, messages


async def check_pr():
  result = await settings.REDIS.blpop("queue", timeout=5)  # type:ignore
  if result is None:
    return None

  _, item = result
  return ScanData.fromBase64(item)


async def scan_code():
  """
  Scan the code
  """
  while (pr_data := await check_pr()) is not None:
    token: str = await jwt.get_installation_token(pr_data.installation_id)

    headers = {
      "Authorization": f"Bearer {token}",
      "Accept": "application/vnd.github.v3.diff",
    }
    resp = await settings.HTTPX.get(
      f"https://api.github.com/repos/{pr_data.repo}/pulls/{pr_data.pr_number}",
      headers=headers,
    )
    if resp.status_code != 200:
      continue

    result = await scan.gitleaks(resp.content)

    # If no secret found leave
    if len(result) == 0:
      return

    await comment.post_comment(
      token, pr_data.repo, pr_data.pr_number, messages.get_secret_found(result)
    )


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
