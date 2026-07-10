from fastapi.testclient import TestClient

from scraper.api.app import app

client = TestClient(app)


def test_episodes_route_exists():
    response = client.get("/episodes")

    assert response.status_code == 200

    data = response.json()

    assert "episodes" in data
    assert isinstance(data["episodes"], list)

def test_episodes_route_supports_pagination():
    response = client.get(
        "/episodes?limit=5&offset=0"
    )

    assert response.status_code == 200

    data = response.json()

    assert "episodes" in data
    assert isinstance(data["episodes"], list)
    assert len(data["episodes"]) <= 5