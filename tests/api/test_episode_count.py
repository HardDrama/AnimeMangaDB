from fastapi.testclient import TestClient

from scraper.api.app import app

client = TestClient(app)


def test_get_episode_count():
    response = client.get("/episodes/count")

    assert response.status_code == 200

    data = response.json()

    assert "episode_count" in data
    assert isinstance(data["episode_count"], int)
    assert data["episode_count"] >= 0