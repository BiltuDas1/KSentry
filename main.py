from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from core import settings


app = FastAPI(
  title="KSentry",
  docs_url=settings.DOCS_URL,
  redoc_url=settings.REDOC_URL,
  openapi_url=settings.OPENAPI_URL,
)


@app.get("/", response_class=HTMLResponse)
def root():
  return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI</title>
    </head>
    <body>
      <p>Hello, World!</p>
    </body>
    </html>
    """


if __name__ == "__main__":
  import uvicorn

  uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=not settings.PRODUCTION)
