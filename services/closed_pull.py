from models import PullRequesPayload
from core import settings
from utils import collaborators, jwt


async def pull_request_closed(payload: PullRequesPayload):
  """
  Remove the pull number from the outdated list
  """
  pull_number = payload.number
  await settings.REDIS.srem("conflicted_pull_request", pull_number)  # type: ignore

  # Get requested_reviewers list and remove them from the pr
  for reviewers in payload.pull_request.requested_reviewers:
    await collaborators.remove_pr(
      username=reviewers.login,
      repo=payload.repository.full_name,
      pr_number=payload.number,
    )

  # Get the actual reviewers and remove them from the pr
  token: str = await jwt.get_installation_token(payload.installation.id)
  url = f"https://api.github.com/repos/{payload.repository.full_name}/pulls/{payload.number}/reviews"
  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }
  response = await settings.HTTPX.get(url=url, headers=headers)
  if response.status_code != 200:
    return

  for reviewers in response.json():
    if reviewers["user"]["type"].lower() != "user":
      continue

    await collaborators.remove_pr(
      username=reviewers["user"]["login"],
      repo=payload.repository.full_name,
      pr_number=payload.number,
    )
