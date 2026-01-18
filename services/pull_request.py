from utils import comment


async def pull_request(payload: dict):
  installation = payload.get("installation")
  if installation is None:
    return
  token = installation.get("id")
  if token is None:
    return
  repository = payload.get("repository")
  if repository is None:
    return
  repo = repository.get("full_name")
  pull_number = payload.get("number")
  if pull_number is None:
    return
  await comment.post_comment(
    token, repo, pull_number, "Thank you for creating this **Pull Request**!"
  )
