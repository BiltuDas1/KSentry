from core import settings


async def add_collaborators(username: str, repo: str):
  await settings.REDIS.hset(f"{repo}:colabs", username, 0)


async def remove_collaborators(username: str, repo: str):
  await settings.REDIS.hdel(f"{repo}:colabs", username)


async def get_users_pr_counts(repo: str) -> dict[str, int] | None:
  return await settings.REDIS.hgetall(f"{repo}:colabs")


async def attach_pr(username: str, repo: str, pr_number: int):
  await settings.REDIS.sadd(f"{repo}:user:{username}", pr_number)
  await settings.REDIS.hincrby(f"{repo}:colabs", username, 1)


async def remove_pr(username: str, repo: str, pr_number: int):
  await settings.REDIS.srem(f"{repo}:user:{username}", pr_number)
  await settings.REDIS.hincrby(f"{repo}:colabs", username, -1)


async def attach_user_to_pr(token: str, username: str, repo: str, pr_number: int):
  url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/requested_reviewers"
  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }

  response = await settings.HTTPX.post(
    url=url, headers=headers, json={"reviewers": [username]}
  )

  if response.status_code == 201:
    return True
  else:
    return False
