from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_list_anime():
    response = client.get("/anime")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if data:
        anime = data[0]

        assert "id" in anime
        assert "title" in anime
        assert "provider" in anime
        assert "base_url" in anime


def test_get_anime_by_id():
    list_response = client.get("/anime")

    assert list_response.status_code == 200

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


def test_list_episodes_for_missing_anime():
    response = client.get(
        "/anime/999999/episodes"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Anime not found.",
    }