from fastapi import FastAPI
from services import pull_request
from fastapi.requests import Request


def Webhook(app: FastAPI):
  @app.post("/")
  async def hook(request: Request):
    payload = await request.json()
    action = payload.get("action")

    if action == "opened":
      await pull_request.pull_request(payload)

    return True
