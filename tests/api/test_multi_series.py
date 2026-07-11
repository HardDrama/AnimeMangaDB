from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_series_endpoint_returns_one_piece_and_naruto():
    response = client.get("/series")

    assert response.status_code == 200

    data = response.json()["series"]
    titles = {
        series["title"]
        for series in data
    }

    assert "One Piece" in titles
    assert "Naruto" in titles


def test_anime_compatibility_returns_multiple_series():
    response = client.get("/anime")

    assert response.status_code == 200

    data = response.json()
    titles = {
        anime["title"]
        for anime in data
    }

    assert "One Piece" in titles
    assert "Naruto" in titles


def test_naruto_episode_list_uses_shared_api_contract():
    anime_response = client.get("/anime")
    anime_list = anime_response.json()

    naruto = next(
        anime
        for anime in anime_list
        if anime["title"] == "Naruto"
    )

    response = client.get(
        f"/anime/{naruto['id']}/episodes"
    )

    assert response.status_code == 200

    episodes = response.json()

    assert len(episodes) == 220

    first_episode = episodes[0]

    assert first_episode["anime_title"] == "Naruto"
    assert first_episode["episode_number"] == 1
    assert first_episode["episode_title"]
    assert first_episode["title"]
    assert "arc" in first_episode


def test_episode_number_route_supports_multiple_series_data():
    response = client.get("/episodes/1")

    assert response.status_code == 200

    data = response.json()

    assert data["episode_number"] == 1
    assert data["anime_title"] in {
        "One Piece",
        "Naruto",
    }


def test_search_returns_multiple_series():
    response = client.get(
        "/search",
        params={"query": "Naruto"},
    )

    assert response.status_code == 200

    data = response.json()

    assert any(
        anime["title"] == "Naruto"
        for anime in data["anime"]
    )