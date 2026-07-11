from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_get_episode_chapters():
    episodes_response = client.get(
        "/episodes?limit=1"
    )

    assert episodes_response.status_code == 200

    episodes = episodes_response.json()["episodes"]

    if not episodes:
        return

    episode_id = episodes[0]["id"]

    response = client.get(
        f"/episodes/{episode_id}/chapters"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for chapter in data:
        assert "chapter_number" in chapter


def test_get_chapters_for_missing_episode():
    response = client.get(
        "/episodes/999999/chapters"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Episode not found.",
    }