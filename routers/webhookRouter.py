from fastapi import FastAPI
from services import is_updated, closed_pull
from fastapi.requests import Request
from models import PullRequesPayload
from utils import verify_signature
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
    payload = PullRequesPayload.model_validate(json.loads(data))

    # Block webhook from bots
    if payload.sender.type == "Bot":
      return False

    if event == "pull_request" and payload.action == "opened":
      await is_updated.check_if_updated(payload)
    elif event == "pull_request" and payload.action == "synchronize":
      await is_updated.updated_again(payload)
    elif event == "pull_request" and payload.action == "closed":
      await closed_pull.pull_request_closed(payload)

    return True
