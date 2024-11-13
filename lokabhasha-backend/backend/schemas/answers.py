from pydantic import BaseModel, ConfigDict
from typing import Optional


class AnswerInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    q_id: int
    resp_id: int
    u_id: int
