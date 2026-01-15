from fastapi import FastAPI
from services import is_updated
from fastapi.requests import Request


def Webhook(app: FastAPI):
  @app.post("/")
  async def hook(request: Request):
    payload = await request.json()
    action = payload.get("action")

    if action == "opened":
      await is_updated.check_if_updated(payload)

    return True
