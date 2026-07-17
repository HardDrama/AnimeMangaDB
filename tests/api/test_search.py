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
    assert "chapter_metadata" in data
    assert isinstance(
        data["chapter_metadata"],
        list,
    )

    assert isinstance(data["anime"], list)
    assert isinstance(data["episodes"], list)
    assert isinstance(data["chapters"], list)


def test_search_anime_includes_counts():
    response = client.get(
        "/search",
        params={"query": "One Piece"},
    )

    assert response.status_code == 200

    data = response.json()

    anime_result = next(
        anime
        for anime in data["anime"]
        if anime["title"] == "One Piece"
    )

    assert isinstance(
        anime_result["episode_count"],
        int,
    )

    assert (
        anime_result["chapter_count"]
        == 1188
    )


def test_search_episode_title():
    response = client.get(
        "/search",
        params={"query": "Luffy"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["episodes"]

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


def test_chapter_metadata_search_includes_series_identity():
    response = client.get(
        "/search",
        params={
            "query": "The Second Critter",
        },
    )

    assert response.status_code == 200

    results = response.json()[
        "chapter_metadata"
    ]

    chapter = next(
        result
        for result in results
        if (
            result["chapter_number"]
            == 10
            and result[
                "chapter_title"
            ]
            == "The Second Critter"
        )
    )

    assert chapter["anime_id"]
    assert (
        chapter["anime_title"]
        == "Naruto"
    )


def test_search_requires_query():
    response = client.get("/search")

    assert response.status_code == 422


def test_numeric_search_matches_episode_number():
    response = client.get(
        "/search",
        params={"query": "50"},
    )

    assert response.status_code == 200

    episodes = response.json()["episodes"]

    assert any(
        episode["episode_number"] == 50
        for episode in episodes
    )


def test_numeric_search_matches_chapter_number():
    response = client.get(
        "/search",
        params={"query": "50"},
    )

    assert response.status_code == 200

    chapters = response.json()["chapters"]

    assert any(
        chapter["chapter_number"] == 50
        for chapter in chapters
    )


def test_search_chapter_metadata_by_title():
    response = client.get(
        "/search",
        params={
            "query": "Romance Dawn",
        },
    )

    assert response.status_code == 200

    results = response.json()[
        "chapter_metadata"
    ]

    assert results

    assert any(
        chapter["chapter_number"] == 1
        and chapter["chapter_title"]
        for chapter in results
    )


def test_search_chapter_metadata_by_arc():
    response = client.get(
        "/search",
        params={
            "query": "Romance Dawn Arc",
        },
    )

    assert response.status_code == 200

    results = response.json()[
        "chapter_metadata"
    ]

    assert results

    assert any(
        chapter["manga_arc"]
        == "Romance Dawn Arc"
        for chapter in results
    )


def test_numeric_chapter_search_keeps_series_identity():
    response = client.get(
        "/search",
        params={
            "query": "50",
        },
    )

    assert response.status_code == 200

    results = [
        chapter
        for chapter in response.json()[
            "chapter_metadata"
        ]
        if (
            chapter["chapter_number"]
            == 50
        )
    ]

    titles = {
        chapter["anime_title"]
        for chapter in results
    }

    assert "One Piece" in titles
    assert "Naruto" in titles

    assert all(
        chapter["anime_id"]
        for chapter in results
    )


def test_numeric_search_returns_scope_v3_chapters():
    response = client.get(
        "/search",
        params={
            "query": "50",
        },
    )

    assert response.status_code == 200

    results = response.json()[
        "chapter_metadata"
    ]

    assert results

    assert all(
        chapter["chapter_number"] == 50
        for chapter in results
        if chapter["chapter_number"] == 50
    )

    assert any(
        chapter["chapter_number"] == 50
        for chapter in results
    )


def test_numeric_search_preserves_scope_v2_mapping_results():
    response = client.get(
        "/search",
        params={
            "query": "50",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "chapters" in data
    assert "chapter_metadata" in data

    assert any(
        result["chapter_number"] == 50
        for result in data["chapters"]
    )

    assert any(
        result["chapter_number"] == 50
        for result in data[
            "chapter_metadata"
        ]
    )


def test_search_naruto_chapter_700_preserves_null_arc():
    response = client.get(
        "/search",
        params={
            "query": "700",
        },
    )

    assert response.status_code == 200

    results = response.json()[
        "chapter_metadata"
    ]

    chapter_700_results = [
        chapter
        for chapter in results
        if chapter["chapter_number"] == 700
    ]

    assert chapter_700_results

    assert any(
        chapter["manga_arc"] is None
        for chapter in chapter_700_results
    )


def test_chapter_metadata_search_without_match_is_empty():
    response = client.get(
        "/search",
        params={
            "query": (
                "NoScopeV3ChapterShouldMatch"
            ),
        },
    )

    assert response.status_code == 200

    assert (
        response.json()[
            "chapter_metadata"
        ]
        == []
    )