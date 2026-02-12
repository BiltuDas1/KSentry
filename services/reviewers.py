from models import PullRequesPayload
from utils import collaborators, jwt
import random


def choose_user(users: list[str], statistics: dict[str, int]):
  if len(users) == 0:
    return None
  if len(users) == 1:
    return users[0]

  start, end = 0, len(users) - 1
  while start < end:
    if statistics[users[start]] > statistics[users[end]]:
      users[start], users[end] = users[end], users[start]
    start += 1
    end -= 1

  end = len(users)
  for i in range(1, len(users)):
    if statistics[users[i - 1]] < statistics[users[i]]:
      end = i
      break

  picked = random.randrange(end)
  return users[picked]


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

  if not success:
    return False

  await collaborators.attach_pr(
    username=user, repo=payload.repository.full_name, pr_number=payload.number
  )

  return True
