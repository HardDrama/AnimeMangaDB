from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def get_anime_by_title(
    title: str,
) -> dict:
    response = client.get(
        "/anime"
    )

    assert response.status_code == 200

    return next(
        anime
        for anime in response.json()
        if anime["title"] == title
    )


def test_get_one_piece_chapter():
    one_piece = get_anime_by_title(
        "One Piece"
    )

    response = client.get(
        f"/anime/{one_piece['id']}/chapters/1"
    )

    assert response.status_code == 200

    chapter = response.json()

    assert chapter["chapter_number"] == 1
    assert chapter["chapter_title"]
    assert chapter["manga_arc"]
    assert chapter["source_url"]
    assert chapter["last_updated"]


def test_get_naruto_chapter():
    naruto = get_anime_by_title(
        "Naruto"
    )

    response = client.get(
        f"/anime/{naruto['id']}/chapters/1"
    )

    assert response.status_code == 200

    chapter = response.json()

    assert chapter["chapter_number"] == 1
    assert chapter["chapter_title"]
    assert chapter["manga_arc"]
    assert chapter["source_url"]
    assert chapter["last_updated"]


def test_naruto_chapter_700_preserves_null_arc():
    naruto = get_anime_by_title(
        "Naruto"
    )

    response = client.get(
        f"/anime/{naruto['id']}/chapters/700"
    )

    assert response.status_code == 200

    chapter = response.json()

    assert chapter["chapter_number"] == 700
    assert chapter["chapter_title"]
    assert chapter["manga_arc"] is None
    assert chapter["source_url"]
    assert chapter["last_updated"]


def test_missing_anime_chapter_detail_returns_404():
    response = client.get(
        "/anime/999999/chapters/1"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Anime not found.",
    }


def test_missing_chapter_returns_404():
    one_piece = get_anime_by_title(
        "One Piece"
    )

    response = client.get(
        f"/anime/{one_piece['id']}/chapters/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Chapter not found.",
    }

def test_invalid_chapter_number_returns_422():
    one_piece = get_anime_by_title(
        "One Piece"
    )

    response = client.get(
        f"/anime/{one_piece['id']}/chapters/not-a-number"
    )

    assert response.status_code == 422