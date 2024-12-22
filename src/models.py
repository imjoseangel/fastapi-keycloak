from typing import Optional
from pydantic import BaseModel


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    preferred_username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
