from fastapi import FastAPI
from routers.webhookRouter import Webhook
from routers.pingRouter import Ping
from core import settings


app = FastAPI(
  title="KSentry",
  docs_url=settings.DOCS_URL,
  redoc_url=settings.REDOC_URL,
  openapi_url=settings.OPENAPI_URL,
  lifespan=settings.lifespan,
)


if settings.SERVERLESS:
  Webhook(app)
else:
  Ping(app)


if __name__ == "__main__":
  import uvicorn

  uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=not settings.PRODUCTION)
