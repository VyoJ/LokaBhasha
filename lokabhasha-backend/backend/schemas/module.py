from pydantic import BaseModel, ConfigDict
from typing import Optional


class ModuleCreate(BaseModel):
    lang_id: int
    name: str
    desc: str
    pre_id: Optional[int] = None


class ModuleUpdate(BaseModel):
    lang_id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    pre_id: Optional[int] = None


class ModuleInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    m_id: int
    lang_id: int
    name: str
    desc: str
    pre_id: Optional[int]
