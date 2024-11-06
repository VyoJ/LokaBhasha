from pydantic import BaseModel
from typing import Optional

class ResourceCreate(BaseModel):
    lang_id: int
    resource_id: int
    url: str
    type: str
    format: str

class ResourceUpdate(BaseModel):
    lang_id: Optional[int] = None
    resource_id: Optional[int] = None
    url: Optional[str] = None
    type: Optional[str] = None
    format: Optional[str] = None

class ResourceInDB(BaseModel):
    lang_id: int
    resource_id: int
    url: str
    type: str
    format: str

    class Config:
        orm_mode = True