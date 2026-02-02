from models.installation import RepositoryAdded
from core import settings
from utils import jwt, collaborators


async def store_collaborators(
  list_of_repos: list[RepositoryAdded], installation_id: int
):
  token: str = await jwt.get_installation_token(installation_id)

  for repo in list_of_repos:
    url = f"https://api.github.com/repos/{repo.full_name}/collaborators"
    headers = {
      "Authorization": f"Bearer {token}",
      "Accept": "application/vnd.github+json",
    }
    response = await settings.HTTPX.get(url=url, headers=headers)

    if response.status_code != 200:
      continue

    usernames = {}
    for user in response.json():
      usernames[user["login"]] = 0

    await collaborators.add_collaborators(repo=repo.full_name, mapping=usernames)
