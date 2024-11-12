from pydantic import BaseModel
from typing import Optional

class APICreate(BaseModel):
    api_url: str
    lang_id: int

class APIUpdate(BaseModel):
    api_id: Optional[int] = None
    api_url: Optional[str] = None
    lang_id: Optional[int] = None

class APIInDB(BaseModel):
    api_id: int
    api_url: str
    lang_id: int

    class Config:
        orm_mode = True