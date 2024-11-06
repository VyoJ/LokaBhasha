from pydantic import BaseModel
from typing import Optional

class APICreate(BaseModel):
    api: str
    lang_id: int

class APIUpdate(BaseModel):
    api: Optional[str] = None
    lang_id: Optional[int] = None

class APIInDB(BaseModel):
    api: str
    lang_id: int

    class Config:
        orm_mode = True