from pydantic import BaseModel
from typing import Optional


class LanguageCreate(BaseModel):
    name: str


class LanguageUpdate(BaseModel):
    name: Optional[str] = None


class LanguageInDB(BaseModel):
    lang_id: int
    name: str

    class Config:
        orm_mode = True
