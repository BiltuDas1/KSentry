from fastapi import FastAPI, BackgroundTasks
from services import scanning


def Ping(app: FastAPI):
  @app.get("/process")
  async def ping(background_tasks: BackgroundTasks):
    background_tasks.add_task(scanning.scan_code)
    return {"status": "Accepted", "message": "Scan started"}
