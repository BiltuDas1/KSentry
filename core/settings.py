from . import debug, environ
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI


PRODUCTION = not debug.DEBUG
DOCS_URL = "/docs" if not PRODUCTION else None
REDOC_URL = "/redoc" if not PRODUCTION else None
OPENAPI_URL = "/openapi.json" if not PRODUCTION else None

# Load APP_PRIVATE_KEY
if not environ.ENV.exist("APP_PRIVATE_KEY"):
  raise EnvironmentError("APP_PRIVATE_KEY Environment can't be empty")
APP_PRIVATE_KEY = str(environ.ENV.get("APP_PRIVATE_KEY"))

# Load APP_ID
if not environ.ENV.exist("APP_ID"):
  raise EnvironmentError("APP_ID Environment can't be empty")
APP_ID = str(environ.ENV.get("APP_ID"))


HTTPX = httpx.AsyncClient()


@asynccontextmanager
async def lifespan(app: FastAPI):
  yield
  await HTTPX.aclose()
