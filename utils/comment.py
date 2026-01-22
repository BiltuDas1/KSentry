from core import settings
from dataclasses import dataclass, asdict


async def post_comment(token: str, repo: str, pull_number: int, message: str):
  """Posts a comment to the specified Pull Request."""
  url = f"https://api.github.com/repos/{repo}/issues/{pull_number}/comments"

  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }

  data = {"body": message}

  response = await settings.HTTPX.post(url, headers=headers, json=data)

  if response.status_code != 201:
    print(f"Failed to post comment: {response.status_code} - {response.text}")


@dataclass(frozen=True)
class CommentData:
  path: str
  line: int
  body: str
  side: str = "RIGHT"


async def comment_on(
  token: str,
  repo: str,
  pull_number: int,
  commit_id: str,
  main_message: str,
  comments: list[CommentData],
):
  """
  Post a comment on the specific line of a specific file
  """
  url = f"https://api.github.com/repos/{repo}/pulls/{pull_number}/reviews"

  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }

  data = {
    "commit_id": commit_id,
    "event": "COMMENT",
    "body": main_message,
    "comments": [],
  }

  for comment in comments:
    data["comments"].append(asdict(comment))

  return await settings.HTTPX.post(url, headers=headers, json=data)
