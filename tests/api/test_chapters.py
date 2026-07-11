from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_get_episodes_for_chapter():
    response = client.get(
        "/chapters/50/episodes"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for episode in data:
        assert "id" in episode
        assert "anime_id" in episode
        assert "anime_title" in episode
        assert "episode_number" in episode
        assert "episode_title" in episode
        assert "title" in episode
        assert "arc" in episode


def test_unmapped_chapter_returns_empty_list():
    response = client.get(
        "/chapters/999999/episodes"
    )

    assert response.status_code == 200
    assert response.json() == []