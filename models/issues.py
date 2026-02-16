from pydantic import BaseModel


class IssueAssignee(BaseModel):
  login: str


class Issue(BaseModel):
  number: int
  assignee: IssueAssignee


class IssueInstallation(BaseModel):
  id: int
