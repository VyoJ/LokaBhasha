from pydantic import BaseModel
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
    q_id: int
    resp_id: int
    u_id: int

    class Config:
        orm_mode = True