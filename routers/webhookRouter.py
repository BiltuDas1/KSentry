from fastapi import FastAPI
from services import is_updated, closed_pull
from fastapi.requests import Request
from models import PullRequesPayload


def Webhook(app: FastAPI):
  @app.post("/")
  async def hook(request: Request):
    payload = PullRequesPayload.model_validate(await request.json())
    event = str(request.headers.get("x-github-event"))

    if event == "pull_request" and payload.action == "opened":
      await is_updated.check_if_updated(payload)
    elif event == "pull_request" and payload.action == "synchronize":
      await is_updated.updated_again(payload)
    elif event == "pull_request" and payload.action == "closed":
      await closed_pull.pull_request_closed(payload)

    return True
