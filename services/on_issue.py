from models import IssuesPayload
from core import settings
from utils import comment, jwt, messages


async def comment_on_threadsold(payload: IssuesPayload, threadsold: int = 3):
  keyname = f"{payload.repository.full_name}:issues:{payload.assignee.login}"
  total_count = await settings.REDIS.scard(keyname)
  if total_count >= threadsold:
    token = await jwt.get_installation_token(payload.installation.id)
    await comment.post_comment(
      token=token,
      repo=payload.repository.full_name,
      pull_number=payload.issue.number,
      message=messages.get_issue_max_comment(
        username=payload.assignee.login, threadsold=threadsold
      ),
    )
