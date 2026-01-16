from fastapi import FastAPI
from routers.webhookRouter import Webhook
from core import settings


app = FastAPI(
  title="KSentry",
  docs_url=settings.DOCS_URL,
  redoc_url=settings.REDOC_URL,
  openapi_url=settings.OPENAPI_URL,
)

Webhook(app)


if __name__ == "__main__":
  import uvicorn

  uvicorn.run("main:app", host="127.0.0.1", port=5001, reload=not settings.PRODUCTION)
