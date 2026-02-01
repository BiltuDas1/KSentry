from pydantic import BaseModel


class Installation(BaseModel):
  id: int
  node_id: str


class Sender(BaseModel):
  login: str
  type: str


class PullRequestHead(BaseModel):
  label: str


class RequestedReviewers(BaseModel):
  login: str


class PullRequest(BaseModel):
  head: PullRequestHead
  requested_reviewers: list[RequestedReviewers]


class Repository(BaseModel):
  full_name: str
  default_branch: str
