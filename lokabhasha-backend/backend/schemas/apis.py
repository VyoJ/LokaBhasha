from pydantic import BaseModel, ConfigDict
from typing import Optional


class APICreate(BaseModel):
    api_url: str
    lang_id: int


class APIUpdate(BaseModel):
    api_id: Optional[int] = None
    api_url: Optional[str] = None
    lang_id: Optional[int] = None


class APIInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    api_id: int
    api_url: str
    lang_id: int
