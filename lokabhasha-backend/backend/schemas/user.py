from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    pref_lang: Optional[int] = None


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    pref_lang: Optional[int] = None


class UserInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    u_id: int
    username: str
    email: str
    joined_on: datetime
    pref_lang: Optional[int] = None
