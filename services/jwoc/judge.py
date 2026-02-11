from core import settings
from . import score
from models import PullRequesPayload
from utils import jwt, comment, messages


async def store_score(payload: PullRequesPayload):
  if not payload.repository.full_name.lower() in settings.JWOC_REPOS:
    return False

  score_earned = score.get_score(payload)
  if score_earned[1] == 0:
    return False

  username = payload.pull_request.user.login

  total_score = await settings.REDIS.hincrby(
    f"{payload.repository.full_name}:leaderboard", username, score_earned[1]
  )

  token: str = await jwt.get_installation_token(payload.installation.id)
  await comment.post_comment(
    token=token,
    repo=payload.repository.full_name,
    pull_number=payload.number,
    message=messages.get_opensource_scoreboard(
      username=username,
      difficulty_level=score_earned[0],
      points_awarded=score_earned[1],
      total_score=total_score,
      max_nums_of_issues_allowed=3,
      project_link=f"https://github.com/{payload.repository.full_name}",
    ),
  )

  return True
