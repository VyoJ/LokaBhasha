# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime


# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str
#     pref_lang: Optional[int] = None


# class UserUpdate(BaseModel):
#     username: Optional[str] = None
#     email: Optional[str] = None
#     password: Optional[str] = None
#     pref_lang: Optional[int] = None


# class UserInDB(BaseModel):
#     u_id: int
#     username: str
#     email: str
#     joined_on: datetime
#     pref_lang: Optional[int] = None

#     class Config:
#         orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    pref_lang: Optional[int] = None
    role: Optional[str] = "user"  # Add role field

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    pref_lang: Optional[int] = None
    role: Optional[str] = None  # Add role field

class UserInDB(BaseModel):
    u_id: int
    username: str
    email: str
    joined_on: datetime
    pref_lang: Optional[int] = None
    role: str  # Add role field

    class Config:
        orm_mode = True