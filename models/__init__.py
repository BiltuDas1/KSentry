from . import pull_request as prequest, compare_branch
from pydantic import BaseModel, TypeAdapter
from typing import List
import base64


class PullRequesPayload(BaseModel):
  action: str
  number: int
  pull_request: prequest.PullRequest
  repository: prequest.Repository
  sender: prequest.Sender
  installation: prequest.Installation


class CompareBranch(BaseModel):
  ahead_by: int
  behind_by: int
  total_commits: int
  files: list[compare_branch.CommittedFileData]


class ScanData(BaseModel):
  repo: str
  default_branch: str
  upstream_branch: str
  installation_id: int
  pr_number: int

  def toBase64(self) -> bytes:
    return base64.b64encode(self.model_dump_json().encode())

  @classmethod
  def fromBase64(cls, data: bytes):
    return ScanData.model_validate_json(base64.b64decode(data).decode())


class GitLeaks(BaseModel):
  StartLine: int
  EndLine: int
  StartColumn: int
  EndColumn: int
  Match: str
  Secret: str
  Entropy: float
