from core import settings


async def create_label(
  token: str, repo: str, label_name: str, label_color: str, label_description: str
):
  """
  Create a new label in Issue/PR

  :param token: The autherization token
  :type token: str
  :param repo: The repo name, format should be username/reponame
  :type repo: str
  :param label_name: The name of the label
  :type label_name: str
  :param label_color: The hex color of the label
  :type label_color: str
  :param label_description: The description of the label
  :type label_description: str
  """
  url = f"https://api.github.com/repos/{repo}/labels"
  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }

  label_data = {
    "name": label_name,
    "color": label_color,
    "description": label_description,
  }

  await settings.HTTPX.post(url, headers=headers, json=label_data)


async def add_label_to_pr(token: str, repo: str, pr_number: int, label_name: str):
  """
  Add a specific label to Issue/PR

  :param token: The authentication token
  :type token: str
  :param repo: The repo name, format should be username/reponame
  :type repo: str
  :param pr_number: Issue/PR Number
  :type pr_number: int
  :param label_name: The name of the label
  :type label_name: str
  """
  url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/labels"

  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }

  # Data must be a list of labels
  data = {"labels": [label_name]}
  await settings.HTTPX.post(url, headers=headers, json=data)


async def remove_label_from_pr(token: str, repo: str, pr_number: int, label_name: str):
  """
  Remove a label from specific Issue/PR

  :param token: The authentication token
  :type token: str
  :param repo: The repo name, format should be username/reponame
  :type repo: str
  :param pr_number: Issue/PR Number
  :type pr_number: int
  :param label_name: The name of the label
  :type label_name: str
  """
  url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/labels/{label_name}"

  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
  }

  await settings.HTTPX.delete(url, headers=headers)
