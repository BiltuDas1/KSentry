from core import settings


async def in_progress(token: str, repo: str, commit_id: str):
  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }

  await settings.HTTPX.post(
    url=f"https://api.github.com/repos/{repo}/statuses/{commit_id}",
    headers=headers,
    json={
      "state": "pending",
      "description": "Scanning code for secrets",
      "context": "KSentry",
    },
  )


async def error(token: str, repo: str, commit_id: str):
  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }

  await settings.HTTPX.post(
    url=f"https://api.github.com/repos/{repo}/statuses/{commit_id}",
    headers=headers,
    json={
      "state": "error",
      "description": "Secrets found! Take actions",
      "context": "KSentry",
    },
  )


async def success(token: str, repo: str, commit_id: str):
  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }

  await settings.HTTPX.post(
    url=f"https://api.github.com/repos/{repo}/statuses/{commit_id}",
    headers=headers,
    json={"state": "success", "description": "No Secret found", "context": "KSentry"},
  )


async def failure(token: str, repo: str, commit_id: str):
  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }

  await settings.HTTPX.post(
    url=f"https://api.github.com/repos/{repo}/statuses/{commit_id}",
    headers=headers,
    json={
      "state": "failure",
      "description": "Bot failed to scan",
      "context": "KSentry",
    },
  )
