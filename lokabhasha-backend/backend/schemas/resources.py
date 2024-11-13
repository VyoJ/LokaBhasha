from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)
    lang_id: int
    resource_id: int
    url: str
    type: str
    format: str
