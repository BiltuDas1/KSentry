from models import PullRequesPayload
from core import settings
from utils import collaborators


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
