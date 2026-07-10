from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_get_episode_by_id():
    response = client.get("/episodes/id/1")

    assert response.status_code in (200, 404)