from fastapi import FastAPI
from services import pull_request
from fastapi.requests import Request


def Webhook(app: FastAPI):
  @app.post("/webhook")
  async def hook(request: Request):
    result = await request.json()
    event = result.get("event")
    payload = result.get("payload")
    action = payload.get("action")

    if event == "pull_request" and action == "opened":
      await pull_request.pull_request(payload)
    
    return True
