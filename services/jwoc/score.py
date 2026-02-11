from models import PullRequesPayload

score = {"easy": 1, "medium": 3, "hard": 5}


def get_score(payload: PullRequesPayload):
  if not payload.pull_request.merged:
    return ("", 0)

  for label in payload.pull_request.labels:
    if label.lower() in score:
      return (label, score[label])

  return ("", 0)
