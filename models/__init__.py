from . import pull_request as prequest
from pydantic import BaseModel


class PullRequesPayload(BaseModel):
  action: str
  number: int
  pull_request: prequest.PullRequest
  repository: prequest.Repository
  sender: prequest.Sender
  installation: prequest.Installation


class CompareBranch(BaseModel):
  behind_by: int
