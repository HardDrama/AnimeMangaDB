from fastapi.testclient import TestClient

from scraper.api.app import app

client = TestClient(app)


def test_episodes_route_exists():
    response = client.get("/episodes")

    assert response.status_code == 200
    assert response.json() == {
        "episodes": [],
    }