from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime, date
from decimal import Decimal


class ModuleProgress(BaseModel):
    lang_id: int
    language_name: str
    module_name: str
    total_questions: int
    answered_questions: int
    module_status: str
    completion_percentage: float


class OverallProgress(BaseModel):
    total_questions: int
    completed_questions: int
    overall_completion_percentage: float


class UserProgress(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    module_progress: List[ModuleProgress]
    overall_progress: OverallProgress


class AdminAnalytics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    daily_responses: int
    most_active_language: str
    active_language_responses: int
    today_signups: int
    overall_avg_latency: float


class UserAnalytics(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total_responses: int
    correct_responses: int
    wrong_responses: int
