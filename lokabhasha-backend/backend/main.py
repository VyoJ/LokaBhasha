from fastapi import FastAPI
from backend.routers import user, language
from backend.utils.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(language.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
