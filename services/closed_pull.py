from models import PullRequesPayload
from core import settings


async def pull_request_closed(payload: PullRequesPayload):
  """
  Remove the pull number from the outdated list
  """
  pull_number = payload.number
  await settings.REDIS.srem("conflicted_pull_request", pull_number)  # type: ignore
