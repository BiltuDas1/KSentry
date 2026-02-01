from fastapi import FastAPI
from services import is_updated, closed_pull, scanning, reviewers
from fastapi.requests import Request
from models import PullRequesPayload, MemberPayload
from utils import verify_signature, collaborators
import json
from core import settings


def Webhook(app: FastAPI):
  @app.post("/")
  async def hook(request: Request):
    data = await request.body()
    sigHeader = str(request.headers.get("x-hub-signature-256"))

    if not verify_signature.verify_signature(data, sigHeader, settings.APP_SECRET):
      return False

    event = str(request.headers.get("x-github-event"))

    if event == "pull_request":
      json_data = json.loads(data)
      payload = PullRequesPayload.model_validate(json_data)

      match payload.action:
        case "opened":
          if await is_updated.check_if_updated(payload):
            await reviewers.add_reviewers(payload)
            await scanning.request_scan(payload)
        case "synchronize":
          if await is_updated.updated_again(payload):
            await scanning.request_scan(payload)
        case "closed":
          await closed_pull.pull_request_closed(payload)
        case "review_requested":
          # On Review: Remove the pr number from the collaborator database
          await collaborators.remove_pr(
            username=json_data["requested_reviewer"]["login"],
            repo=payload.repository.full_name,
            pr_number=payload.number,
          )
    elif event == "member":
      payload = MemberPayload.model_validate(json.loads(data))

      match payload.action:
        case "added":
          await collaborators.add_collaborators(
            username=payload.member.login, repo=payload.repository.full_name
          )
        case "removed":
          await collaborators.remove_collaborators(
            username=payload.member.login, repo=payload.repository.full_name
          )

    return True
