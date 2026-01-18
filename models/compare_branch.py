from pydantic import BaseModel
from typing import Literal


class CommittedFileData(BaseModel):
  status: Literal["added", "removed", "modified"]
  filename: str
  raw_url: str
