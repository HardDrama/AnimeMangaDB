from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_get_scope():
    response = client.get("/scope")

    assert response.status_code == 200

    assert response.json() == {
        "scope": "v3",
        "supported_scopes": [
            "v2",
            "v3",
        ],
        "compatibility": {
            "scope_v2": True,
        },
        "fields": {
            "anime": [
                "episode_number",
                "episode_title",
                "arc",
            ],
            "manga": [
                "chapter_number",
            ],
            "chapter_metadata": [
                "chapter_number",
                "chapter_title",
                "manga_arc",
                "source_url",
                "last_updated",
            ],
        },
    }

def test_scope_v3_metadata_fields_are_exposed():
    response = client.get("/scope")

    assert response.status_code == 200

    data = response.json()

    assert data["scope"] == "v3"

    assert data["compatibility"][
        "scope_v2"
    ] is True

    assert data["fields"][
        "chapter_metadata"
    ] == [
        "chapter_number",
        "chapter_title",
        "manga_arc",
        "source_url",
        "last_updated",
    ]