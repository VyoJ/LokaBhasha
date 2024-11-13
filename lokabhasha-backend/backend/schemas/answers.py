from pydantic import BaseModel, ConfigDict
from typing import Optional


class AnswerCreate(BaseModel):
    q_id: int
    resp_id: int
    u_id: int


class AnswerUpdate(BaseModel):
    q_id: Optional[int] = None
    resp_id: Optional[int] = None
    u_id: Optional[int] = None


class AnswerInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    q_id: int
    resp_id: int
    u_id: int