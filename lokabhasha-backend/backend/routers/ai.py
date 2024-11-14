from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File
from backend.schemas.ai import (
    AudioToTextResponse,
    TextToSpeechRequest,
    TextToSpeechResponse,
    AnswerCompareRequest,
    AnswerCompareResponse,
)
from groq import Groq
import os
import requests

router = APIRouter()
groq_client = None


def initialize_groq():
    global groq_client
    if groq_client is None:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        groq_client = Groq(api_key=groq_api_key)


@router.on_event("startup")
async def startup_event():
    initialize_groq()


@router.post("/speech-to-text", response_model=AudioToTextResponse)
async def convert_speech_to_text(audio: UploadFile = File(...)):
    """Convert speech audio to text using Groq"""
    if not groq_client:
        raise HTTPException(status_code=500, detail="Groq client not initialized")

    try:
        audio_content = await audio.read()
        translation = groq_client.audio.translations.create(
            file=("recording.wav", audio_content),
            model="whisper-large-v3",
            prompt="Specify context or spelling",
            response_format="json",
            temperature=0.0,
        )
        return AudioToTextResponse(transcribed=translation.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")


@router.post("/text-to-speech", response_model=TextToSpeechResponse)
async def convert_text_to_speech(request: TextToSpeechRequest):
    """Convert text to speech using Sarvam AI"""
    try:
        url = "https://api.sarvam.ai/text-to-speech"

        payload = {
            "inputs": [request.text],
            "target_language_code": "hi-IN",
            "speaker": "meera",
            "pitch": 0,
            "pace": 1.2,
            "loudness": 1.5,
            "speech_sample_rate": 8000,
            "enable_preprocessing": True,
            "model": "bulbul:v1",
        }

        headers = {
            "Content-Type": "application/json",
            "api-subscription-key": f"{os.getenv('SARVAM_KEY')}",
        }

        response = requests.post(url, json=payload, headers=headers)
        return TextToSpeechResponse(audio=response.json()["audios"][0])

    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=500, detail=f"Error converting text to speech: {str(e)}"
        )


@router.post("/compare-answers", response_model=AnswerCompareResponse)
async def compare_answers(request: AnswerCompareRequest):
    """Compare expected and user answers using LLaMA model"""
    if not groq_client:
        raise HTTPException(status_code=500, detail="Groq client not initialized")

    try:
        prompt = f"""Compare these two answers and respond with only 'Yes' or 'No' if they are semantically similar:

Expected answer: {request.expected_answer}
User answer: {request.user_answer}

Are they similar? Answer with just Yes or No:"""

        completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a language assessor. You get two sentences and respond only with 'Yes' or 'No'. if they are kind of similar or not",
                },
                {"role": "user", "content": prompt},
            ],
            model="llama-3.1-70b-versatile",
            temperature=0.1,
            max_tokens=10,
            top_p=1,
        )

        response = completion.choices[0].message.content.strip().lower()
        print(response)
        return AnswerCompareResponse(is_similar=(response == "yes"))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error comparing answers: {str(e)}"
        )
