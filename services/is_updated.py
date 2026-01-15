from core import settings
from utils import pull_comment


async def check_if_updated(payload: dict):
  """
  Checks if the Requested branch is up-to-date with the main branch.
  If not then send a comment to update the branch
  """
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
  if repo is None:
    return
  default_branch = repository.get("default_branch")
  if default_branch is None:
    return
  pull_number = payload.get("number")
  if pull_number is None:
    return
  pull_request = payload.get("pull_request")
  if pull_request is None:
    return
  head = pull_request.get("head")
  if head is None:
    return
  label = head.get("label")
  if label is None:
    return

  response = await settings.HTTPX.get(
    f"https://api.github.com/repos/{repo}/compare/{default_branch}...{label}"
  )
  if response.status_code != 201:
    return
  data = response.json()
  behind_by = data.get("behind_by")
  if behind_by is None:
    return
  if behind_by > 0:
    await pull_comment.post_comment(
      token,
      repo,
      pull_number,
      f"Your branch is not up-to-date with `{default_branch}` branch. You should update it.",
    )
