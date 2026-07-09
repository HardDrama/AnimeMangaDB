from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_get_version():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "api_version": "0.52.0",
        "platform_checkpoint": "v2 (in progress)",
        "supported_scope": "v2",
    }