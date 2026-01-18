from . import messages
from models import GitLeaks
from utils import redact


def get_outdated_upstream(upstream_branch_name: str, upstream_repo: str):
  """
  Get the message body of the Pull Request comment when the branch is not uptodate with the upstream branch

  :param upstream_branch_name: Name of the upstream branch, branch name only
  :type upstream_branch_name: str
  :param upstream_repo: The repo name of the origin, Should be in this format username/reponame
  :type upstream_repo: str
  """
  return messages.PULL_OUTDATED_UPSTREAM.format(
    upstream_branch_name=upstream_branch_name, upstream_repo=upstream_repo
  )


def get_outdated_upstream_again(upstream_branch_name: str):
  """
  Get the message body of the Outdated Pull Request Comment, when the user created new commits but still it's not uptodate with origin

  :param upstream_branch_name: Name of the upstream branch, branch name only
  :type upstream_branch_name: str
  """
  return messages.PULL_OUTDATED_UPSTREAM_AGAIN.format(
    upstream_branch_name=upstream_branch_name
  )


def get_secret_found(secrets_data: list[GitLeaks]):
  """
  Get the message body of the Secret Found Comment
  """
  data = []
  for leak in secrets_data:
    data.append(
      messages.SECRET_CODEBLOCK.format(
        filename=leak.File,
        line_num=leak.StartLine,
        redact_code=redact.replace_redact(
          redact.redact_text(leak.Secret), leak.Secret, leak.Match
        ),
      )
    )

  return messages.SECRET_FOUND.format(secrets_data="\n".join(data))
