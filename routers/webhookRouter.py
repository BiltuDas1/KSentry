from fastapi import FastAPI
from services import is_updated, closed_pull, scanning, reviewers, installation, jwoc
from fastapi.requests import Request
from models import (
  PullRequesPayload,
  MemberPayload,
  InstallationPayload,
  InstallationDefaultPayload,
)
from utils import verify_signature, collaborators
import json
from core import settings


def Webhook(app: FastAPI):
  @app.post("/")
  async def hook(request: Request):
    data = await request.body()
    json_data = json.loads(data)
    sigHeader = str(request.headers.get("x-hub-signature-256"))

    if not verify_signature.verify_signature(data, sigHeader, settings.APP_SECRET):
      return False

    event = str(request.headers.get("x-github-event"))

    if event == "pull_request":
      payload = PullRequesPayload.model_validate(json_data)
      if payload.repository.owner.login.lower() not in settings.ALLOWED_USERS:
        return False

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
          await jwoc.store_score(payload)
        case "review_requested":
          # On Review: Attach the pr number in the collaborator database
          await collaborators.attach_pr(
            username=json_data["requested_reviewer"]["login"],
            repo=payload.repository.full_name,
            pr_number=payload.number,
          )
        case "review_request_removed":
          # On Review: Remove the pr number from the collaborator database
          await collaborators.remove_pr(
            username=json_data["requested_reviewer"]["login"],
            repo=payload.repository.full_name,
            pr_number=payload.number,
          )
    elif event == "member":
      payload = MemberPayload.model_validate(json_data)
      if payload.repository.owner.login.lower() not in settings.ALLOWED_USERS:
        return False

      match payload.action:
        case "added":
          await collaborators.add_collaborators(
            username=payload.member.login, repo=payload.repository.full_name
          )
        case "removed":
          await collaborators.remove_collaborators(
            username=payload.member.login, repo=payload.repository.full_name
          )
    elif event == "installation":
      payload = InstallationDefaultPayload.model_validate(json_data)
      if payload.action == "created":
        await installation.store_collaborators(
          list_of_repos=payload.repositories, installation_id=payload.installation.id
        )
    elif event == "installation_repositories":
      payload = InstallationPayload.model_validate(json_data)
      if payload.action == "added":
        await installation.store_collaborators(
          list_of_repos=payload.repositories_added,
          installation_id=payload.installation.id,
        )

    return True
