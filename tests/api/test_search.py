from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_search_returns_expected_structure():
    response = client.get(
        "/search",
        params={"query": "One Piece"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "anime" in data
    assert "episodes" in data
    assert "chapters" in data

    assert isinstance(data["anime"], list)
    assert isinstance(data["episodes"], list)
    assert isinstance(data["chapters"], list)


def test_search_episode_title():
    response = client.get(
        "/search",
        params={"query": "Luffy"},
    )

    assert response.status_code == 200

    data = response.json()

    for episode in data["episodes"]:
        assert "anime_id" in episode
        assert "anime_title" in episode
        assert "episode_number" in episode
        assert "episode_title" in episode
        assert "title" in episode


def test_search_by_chapter_number():
    response = client.get(
        "/search",
        params={"query": "1"},
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["chapters"], list)

    for chapter in data["chapters"]:
        assert "chapter_number" in chapter
        assert "episodes" in chapter


def test_search_requires_query():
    response = client.get("/search")

    assert response.status_code == 422