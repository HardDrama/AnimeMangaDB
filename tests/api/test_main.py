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

    body = response.json()

    assert isinstance(body, list)

def test_episodes_endpoint():
    response = client.get("/episodes")

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)

def test_anime_detail_not_found():
    response = client.get("/anime/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Anime not found"
    }

def test_episode_detail_not_found():
    response = client.get("/episodes/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Episode not found"
    }

def test_episode_lookup_by_anime_and_number_not_found():
    response = client.get("/anime/999999/episodes/1")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Episode not found"
    }

def test_episode_chapters_endpoint():
    response = client.get("/episodes/999999/chapters")

    assert response.status_code == 200
    assert response.json() == []

def test_anime_episodes_endpoint():
    response = client.get("/anime/999999/episodes")

    assert response.status_code == 200
    assert response.json() == []

def test_chapter_lookup_endpoint():
    response = client.get("/chapters/999999/episodes")

    assert response.status_code == 200
    assert response.json() == []