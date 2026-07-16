from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_list_anime():
    response = client.get("/anime")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert "chapter_count" in anime
    assert isinstance(
        anime["chapter_count"],
        int,
    )

    if data:
        anime = data[0]

        assert "id" in anime
        assert "title" in anime
        assert "provider" in anime
        assert "base_url" in anime
        assert "episode_count" in anime
        assert isinstance(anime["episode_count"], int)


def test_get_anime_by_id():
    list_response = client.get("/anime")

    assert list_response.status_code == 200

    assert "episode_count" in data
    assert "chapter_count" in data

    assert isinstance(
        data["episode_count"],
        int,
    )

    assert isinstance(
        data["chapter_count"],
        int,
    )

    anime_list = list_response.json()

    if not anime_list:
        return

    anime_id = anime_list[0]["id"]

    response = client.get(
        f"/anime/{anime_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == anime_id
    assert "title" in data


def test_get_missing_anime():
    response = client.get(
        "/anime/999999"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Anime not found.",
    }

def test_list_episodes_for_anime():
    list_response = client.get("/anime")

    assert list_response.status_code == 200

    anime_list = list_response.json()

    if not anime_list:
        return

    anime_id = anime_list[0]["id"]

    response = client.get(
        f"/anime/{anime_id}/episodes"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if data:
        episode = data[0]

        assert "id" in episode
        assert "anime_title" in episode
        assert "episode_number" in episode
        assert "episode_title" in episode
        assert "arc" in episode
        assert "source_url" in episode
        assert "anime_id" in episode
        assert "title" in episode
        assert episode["title"] == episode["episode_title"]


def test_list_episodes_for_missing_anime():
    response = client.get(
        "/anime/999999/episodes"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Anime not found.",
    }

def test_anime_summary_includes_certified_counts():
    response = client.get("/anime")

    assert response.status_code == 200

    anime_by_title = {
        anime["title"]: anime
        for anime in response.json()
    }

    assert (
        anime_by_title[
            "One Piece"
        ]["chapter_count"]
        == 1188
    )

    assert (
        anime_by_title[
            "Naruto"
        ]["chapter_count"]
        == 700
    )