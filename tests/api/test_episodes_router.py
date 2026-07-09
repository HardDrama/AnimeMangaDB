from fastapi.testclient import TestClient

from scraper.api.app import app

client = TestClient(app)


def test_episodes_route_exists():
    response = client.get("/episodes")

    assert response.status_code == 200

    data = response.json()

    assert "episodes" in data
    assert isinstance(data["episodes"], list)