from pydantic import BaseModel
from typing import List


class AudioToTextResponse(BaseModel):
    transcribed: str


class TextToSpeechRequest(BaseModel):
    text: str


class TextToSpeechResponse(BaseModel):
    audio: str


class AnswerCompareRequest(BaseModel):
    expected_answer: str
    user_answer: str


class AnswerCompareResponse(BaseModel):
    is_similar: bool
