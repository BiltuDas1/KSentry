from pydantic import BaseModel


class RepositoryAdded(BaseModel):
  full_name: str


class AccountPayload(BaseModel):
  login: str


class InstallationPayload(BaseModel):
  id: int
  account: AccountPayload
