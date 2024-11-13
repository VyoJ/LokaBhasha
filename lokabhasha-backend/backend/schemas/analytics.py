from pydantic import BaseModel, ConfigDict
from typing import Optional


class AdminAnalytics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    pass


class UserAnalytics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    pass


class UserProgress(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    pass
