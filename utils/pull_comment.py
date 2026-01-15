from . import jwt
from core import settings


async def post_comment(installation_id: int, repo: str, pull_number: int, message: str):
  """Posts a comment to the specified Pull Request."""
  url = f"https://api.github.com/repos/{repo}/issues/{pull_number}/comments"

  token = await jwt.get_installation_token(installation_id)

  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }

  data = {"body": message}

  response = await settings.HTTPX.post(url, headers=headers, json=data)

  if response.status_code != 201:
    print(f"Failed to post comment: {response.status_code} - {response.text}")
