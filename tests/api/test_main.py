import sys
from pathlib import Path

from fastapi.testclient import TestClient


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "AnimeMangaDB API is running"
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "application": "AnimeMangaDB",
        "version": "0.29.0",
    }


def test_version_endpoint():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "version": "0.29.0"
    }

def test_anime_endpoint():
    response = client.get("/anime")

    assert response.status_code == 200
    assert response.json() == {
        "anime": []
    }