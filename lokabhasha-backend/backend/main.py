from fastapi import FastAPI
from backend.routers import user, language, apis, module, question, resources, responses, answers
from backend.utils.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(language.router)
app.include_router(user.router)
app.include_router(apis.router)
app.include_router(module.router)
app.include_router(question.router)
app.include_router(resources.router)
app.include_router(responses.router)
app.include_router(answers.router)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
