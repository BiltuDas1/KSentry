from core import settings
from utils import jwt, pr_label, pull_comment, messages
from models import PullRequesPayload, CompareBranch


async def check_if_updated(payload: PullRequesPayload):
  """
  Checks if the Requested branch is up-to-date with the main branch.
  If not then send a comment to update the branch
  """
  installation_id = payload.installation.id
  repo = payload.repository.full_name
  default_branch = payload.repository.default_branch
  pull_number = payload.number
  label = payload.pull_request.head.label

  response = await settings.HTTPX.get(
    f"https://api.github.com/repos/{repo}/compare/{default_branch}...{label}"
  )
  if response.status_code != 200:
    return

  data = CompareBranch.model_validate(response.json())
  if data.behind_by > 0:
    token: str = await jwt.get_installation_token(installation_id)

    await settings.REDIS.sadd("conflicted_pull_request", pull_number)  # type: ignore
    await pr_label.create_label(
      token, repo, "outdated", "cfd3d7", "The Pull Request is outdated"
    )
    await pr_label.add_label_to_pr(token, repo, pull_number, "outdated")
    await pull_comment.post_comment(
      token, repo, pull_number, messages.get_outdated_upstream(default_branch, repo)
    )


async def updated_again(payload: PullRequesPayload):
  """
  Re-check if the branch is merge properly or not, if not then send message to merge again,
  if merge successful then remove outdated label from pr
  """
  installation_id = payload.installation.id
  repo = payload.repository.full_name
  default_branch = payload.repository.default_branch
  label = payload.pull_request.head.label
  pull_number = payload.number

  exist = await settings.REDIS.sismember("conflicted_pull_request", pull_number)  # type: ignore
  if not exist:
    return

  response = await settings.HTTPX.get(
    f"https://api.github.com/repos/{repo}/compare/{default_branch}...{label}"
  )
  if response.status_code != 200:
    return

  data = CompareBranch.model_validate(response.json())
  token: str = await jwt.get_installation_token(installation_id)
  if data.behind_by > 0:
    await pull_comment.post_comment(
      token, repo, pull_number, messages.get_outdated_upstream_again(default_branch)
    )
  else:
    await settings.REDIS.srem("conflicted_pull_request", pull_number)  # type: ignore
    await pr_label.remove_label_from_pr(token, repo, pull_number, "outdated")
