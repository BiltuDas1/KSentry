from models import PullRequesPayload
from utils import collaborators, jwt
import random


def choose_user(users: list[str], statistics: dict[str, int]):
  """
  Selects a user with the lowest workload.
  If multiple users have the same minimum workload, it picks one randomly.
  """
  if not users:
    return None

  min_workload = min(statistics[u] for u in users)
  candidates = [u for u in users if statistics[u] == min_workload]

  return random.choice(candidates)


async def add_reviewers(payload: PullRequesPayload):
  statistics = await collaborators.get_users_pr_counts(payload.repository.full_name)
  if statistics is None:
    return False

  # Remove the user which opened the pull request
  users: list[str] = []
  for username in statistics.keys():
    if payload.sender.login != username:
      users.append(username)

  # If all have same load then pick random
  # Otherwise pick the one user which have low load
  # If multiple users have low load then pick randomly among them
  print(users, flush=True)
  print(statistics, flush=True)
  user = choose_user(users, statistics)
  if user is None:
    return False

  token: str = await jwt.get_installation_token(payload.installation.id)

  success = await collaborators.attach_user_to_pr(
    token=token,
    username=user,
    repo=payload.repository.full_name,
    pr_number=payload.number,
  )

  return success
