from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_get_scope():
    response = client.get("/scope")

    assert response.status_code == 200
    assert response.json() == {
        "scope": "v2",
        "fields": {
            "anime": [
                "episode_number",
                "episode_title",
                "arc",
            ],
            "manga": [
                "chapter_number",
            ],
        },
    }