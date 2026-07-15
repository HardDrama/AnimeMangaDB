from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def get_one_piece() -> dict:
    response = client.get(
        "/anime"
    )

    assert response.status_code == 200

    return next(
        anime
        for anime in response.json()
        if anime["title"] == "One Piece"
    )


def test_one_piece_scope_v3_chapter_coverage():
    one_piece = get_one_piece()

    response = client.get(
        f"/anime/{one_piece['id']}/chapters"
    )

    assert response.status_code == 200

    chapters = response.json()

    assert len(chapters) == 1188

    chapter_numbers = [
        chapter["chapter_number"]
        for chapter in chapters
    ]

    assert chapter_numbers == list(
        range(
            1,
            1189,
        )
    )


def test_one_piece_scope_v3_required_metadata_complete():
    one_piece = get_one_piece()

    response = client.get(
        f"/anime/{one_piece['id']}/chapters"
    )

    assert response.status_code == 200

    chapters = response.json()

    assert all(
        chapter["chapter_title"]
        for chapter in chapters
    )

    assert all(
        chapter["manga_arc"]
        for chapter in chapters
    )

    assert all(
        chapter["source_url"]
        for chapter in chapters
    )

    assert all(
        chapter["last_updated"]
        for chapter in chapters
    )


def test_one_piece_scope_v3_boundary_chapters():
    one_piece = get_one_piece()

    first_response = client.get(
        f"/anime/{one_piece['id']}/chapters/1"
    )

    last_response = client.get(
        f"/anime/{one_piece['id']}/chapters/1188"
    )

    assert first_response.status_code == 200
    assert last_response.status_code == 200

    first_chapter = first_response.json()
    last_chapter = last_response.json()

    assert first_chapter["chapter_number"] == 1
    assert first_chapter["chapter_title"]
    assert first_chapter["manga_arc"]
    assert first_chapter["source_url"]
    assert first_chapter["last_updated"]

    assert last_chapter["chapter_number"] == 1188
    assert last_chapter["chapter_title"]
    assert last_chapter["manga_arc"]
    assert last_chapter["source_url"]
    assert last_chapter["last_updated"]


def test_one_piece_scope_v3_list_and_detail_match():
    one_piece = get_one_piece()

    list_response = client.get(
        f"/anime/{one_piece['id']}/chapters"
    )

    detail_response = client.get(
        f"/anime/{one_piece['id']}/chapters/50"
    )

    assert list_response.status_code == 200
    assert detail_response.status_code == 200

    list_chapter = next(
        chapter
        for chapter in list_response.json()
        if chapter["chapter_number"] == 50
    )

    detail_chapter = detail_response.json()

    assert detail_chapter == list_chapter


def test_one_piece_scope_v3_title_search():
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

    assert any(
        chapter["chapter_number"] == 1
        and chapter["chapter_title"]
        for chapter in results
    )


def test_one_piece_scope_v3_arc_search():
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

    assert any(
        chapter["manga_arc"]
        == "Romance Dawn Arc"
        for chapter in results
    )


def test_one_piece_scope_v3_numeric_search():
    response = client.get(
        "/search",
        params={
            "query": "1188",
        },
    )

    assert response.status_code == 200

    results = response.json()[
        "chapter_metadata"
    ]

    assert any(
        chapter["chapter_number"] == 1188
        for chapter in results
    )