from core import settings


async def compare_branch(token: str, repo, default_branch, pr_branch):
  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }

  response = await settings.HTTPX.get(
    f"https://api.github.com/repos/{repo}/compare/{default_branch}...{pr_branch}",
    headers=headers,
  )

  if response.status_code == 200:
    return response
