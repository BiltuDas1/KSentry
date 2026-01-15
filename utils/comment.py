import httpx


def post_comment(installation_token: int, repo: str, pull_number: int, message: str):
  """Posts a comment to the specified Pull Request."""
  url = f"https://api.github.com/repos/{repo}/issues/{pull_number}/comments"

  headers = {
    "Authorization": f"Bearer {installation_token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
  }

  data = {"body": message}

  response = httpx.post(url, headers=headers, json=data)

  if response.status_code != 201:
    print(f"Failed to post comment: {response.status_code} - {response.text}")
