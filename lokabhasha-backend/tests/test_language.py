import pytest
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.utils.database import Base, get_db

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = "lokabhasha_test"

encoded_password = quote_plus(DB_PASSWORD)

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield


def test_create_language(test_db):
    response = client.post("/languages/", json={"name": "hi"})
    assert response.status_code == 200
    assert response.json()["name"] == "hi"


def test_read_languages(test_db):
    response = client.get("/languages/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_read_language(test_db):
    response = client.get("/languages/1")
    assert response.status_code == 200
    assert response.json()["name"] == "hi"


def test_update_language(test_db):
    response = client.put("/languages/1", json={"name": "Hindi"})
    assert response.status_code == 200
    assert response.json()["name"] == "Hindi"


def test_delete_language(test_db):
    response = client.delete("/languages/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Hindi"
    response = client.get("/languages/1")
    assert response.status_code == 404
