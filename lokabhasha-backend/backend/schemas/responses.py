from pydantic import BaseModel, ConfigDict
from typing import Optional

class ResponseCreate(BaseModel):
    response_asr: str
    response_url: str
    response_translate: str
    latency: int

class ResponseUpdate(BaseModel):
    response_asr: Optional[str] = None
    response_url: Optional[str] = None
    response_translate: Optional[str] = None
    latency: Optional[int] = None

class ResponseInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    resp_id: int
    response_asr: str
    response_url: str
    response_translate: str
    latency: int