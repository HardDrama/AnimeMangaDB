from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def test_list_series():
    response = client.get("/series")

    assert response.status_code == 200

    data = response.json()

    assert "series" in data
    assert isinstance(
        data["series"],
        list,
    )

    for series in data["series"]:
        assert "id" in series
        assert "title" in series
        assert "provider" in series
        assert "episode_count" in series
        assert "chapter_count" in series

        assert isinstance(
            series["episode_count"],
            int,
        )

        assert isinstance(
            series["chapter_count"],
            int,
        )


def test_list_series_includes_certified_chapter_counts():
    response = client.get("/series")

    assert response.status_code == 200

    series_by_title = {
        series["title"]: series
        for series in response.json()[
            "series"
        ]
    }

    assert (
        series_by_title[
            "One Piece"
        ]["chapter_count"]
        == 1188
    )

    assert (
        series_by_title[
            "Naruto"
        ]["chapter_count"]
        == 700
    )