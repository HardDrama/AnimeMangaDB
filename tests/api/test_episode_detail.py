from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_get_episode_placeholder():
    response = client.get("/episodes/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 0,
        "anime_title": "Unknown",
        "episode_number": 1,
        "episode_title": None,
        "arc": None,
        "source_url": None,
    }