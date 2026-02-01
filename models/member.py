from pydantic import BaseModel


class Member(BaseModel):
  login: str


class Repository(BaseModel):
  full_name: str
