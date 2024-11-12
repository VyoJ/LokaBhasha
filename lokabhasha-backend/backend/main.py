from fastapi import FastAPI
from backend.routers import (
    language,
    user,
    apis,
    module,
    question,
    resources,
    responses,
    answers,
    auth,
)
from backend.utils.database import engine, Base
from backend.models.language import Language
from backend.models.user import User

app = FastAPI()


app.include_router(language.router)
app.include_router(user.router)
app.include_router(apis.router)
app.include_router(module.router)
app.include_router(question.router)
app.include_router(resources.router)
app.include_router(responses.router)
app.include_router(answers.router)
app.include_router(auth.router, prefix="/auth")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
