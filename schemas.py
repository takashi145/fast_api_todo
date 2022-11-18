from pydantic import BaseModel
from typing import Optional
from decouple import config

CSRF_KEY = config('CSRF_KEY')

class TodoResponse(BaseModel):
  id: str
  title: str
  description: str

class TodoRequest(BaseModel):
  title: str
  description: str

class SuccessMessage(BaseModel):
  message: str

class UserRequest(BaseModel):
  email: str
  password: str


class UserInfo(BaseModel):
  id: Optional[str] = None # 任意の値
  email: str

class CsrfSettings(BaseModel):
  secret_key: str = CSRF_KEY

class Csrf(BaseModel):
  csrf_token: str
