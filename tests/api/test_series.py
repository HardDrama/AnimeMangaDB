from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_list_series():
    response = client.get("/series")

    assert response.status_code == 200

    data = response.json()

    assert "series" in data
    assert isinstance(data["series"], list)