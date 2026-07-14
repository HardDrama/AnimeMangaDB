from types import SimpleNamespace

from fastapi.testclient import TestClient

from scraper.api.app import app
from scraper.api.routes import anime as anime_routes


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


def test_one_piece_chapter_list():
    one_piece = get_anime_by_title(
        "One Piece"
    )

    response = client.get(
        f"/anime/{one_piece['id']}/chapters"
    )

    assert response.status_code == 200

    chapters = response.json()

    assert len(chapters) == 1188

    assert (
        chapters[0]["chapter_number"]
        == 1
    )

    assert (
        chapters[-1]["chapter_number"]
        == 1188
    )

    first_chapter = chapters[0]

    assert "chapter_title" in first_chapter
    assert "manga_arc" in first_chapter
    assert "source_url" in first_chapter
    assert "last_updated" in first_chapter


def test_naruto_chapter_list():
    naruto = get_anime_by_title(
        "Naruto"
    )

    response = client.get(
        f"/anime/{naruto['id']}/chapters"
    )

    assert response.status_code == 200

    chapters = response.json()

    assert len(chapters) == 700

    chapter_numbers = [
        chapter["chapter_number"]
        for chapter in chapters
    ]

    assert chapter_numbers == list(
        range(
            1,
            701,
        )
    )


def test_naruto_chapter_700_preserves_null_arc():
    naruto = get_anime_by_title(
        "Naruto"
    )

    response = client.get(
        f"/anime/{naruto['id']}/chapters"
    )

    assert response.status_code == 200

    chapter_700 = next(
        chapter
        for chapter in response.json()
        if chapter["chapter_number"] == 700
    )

    assert chapter_700["chapter_title"]
    assert chapter_700["manga_arc"] is None
    assert chapter_700["source_url"]
    assert chapter_700["last_updated"]


def test_missing_anime_chapter_list_returns_404():
    response = client.get(
        "/anime/999999/chapters"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Anime not found.",
    }


def test_valid_anime_without_chapters_returns_empty_list(
    monkeypatch,
):
    class FakeSession:
        def close(self):
            pass

    class FakeRepository:
        def __init__(
            self,
            session,
        ):
            self.session = session

        def get_anime_by_id(
            self,
            anime_id,
        ):
            return SimpleNamespace(
                id=anime_id,
                title="Empty Test Anime",
            )

        def list_chapter_metadata(
            self,
            anime_id,
        ):
            return []

    monkeypatch.setattr(
        anime_routes,
        "SessionLocal",
        lambda: FakeSession(),
    )

    monkeypatch.setattr(
        anime_routes,
        "EpisodeRepository",
        FakeRepository,
    )

    response = client.get(
        "/anime/999/chapters"
    )

    assert response.status_code == 200
    assert response.json() == []