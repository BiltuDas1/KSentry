from pydantic import BaseModel


class Installation(BaseModel):
  id: int
  node_id: str


class Sender(BaseModel):
  type: str


class PullRequestHead(BaseModel):
  label: str


class PullRequest(BaseModel):
  head: PullRequestHead


class Repository(BaseModel):
  full_name: str
  default_branch: str
