import sys
from types import SimpleNamespace

from tools import ingest_chapter_metadata


class FakeSession:
    def close(self):
        pass


class FakeRepository:
    anime = SimpleNamespace(
        id=1,
        title="One Piece",
        provider="fandom",
    )

    def __init__(
        self,
        session,
    ):
        self.session = session

    def get_anime_by_title(
        self,
        title,
    ):
        if title == "One Piece":
            return self.anime

        return None

    def get_chapter_metadata(
        self,
        anime_id,
        chapter_number,
    ):
        return None


class FakeIngestionService:
    def __init__(
        self,
        discovery_service,
        provider,
        repository,
    ):
        pass

    def ingest(
        self,
        anime,
        chapter_number,
    ):
        return SimpleNamespace(
            chapter_number=chapter_number,
            chapter_title="Test Chapter",
            manga_arc="Test Arc",
            source_url="https://example.com/chapter/1",
        )


def configure_successful_ingestion(
    monkeypatch,
):
    monkeypatch.setattr(
        ingest_chapter_metadata,
        "SessionLocal",
        lambda: FakeSession(),
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "EpisodeRepository",
        FakeRepository,
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "BrowserClient",
        lambda: object(),
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "load_provider_config",
        lambda path: object(),
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "ChapterUrlDiscoveryService",
        lambda config, browser_client: object(),
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "create_chapter_metadata_provider",
        lambda **kwargs: object(),
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "ChapterMetadataIngestionService",
        FakeIngestionService,
    )


def test_ingestion_cli_success(
    monkeypatch,
    capsys,
):
    configure_successful_ingestion(
        monkeypatch
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ingest_chapter_metadata",
            "--anime",
            "One Piece",
            "--chapter",
            "1",
        ],
    )

    ingest_chapter_metadata.main()

    output = capsys.readouterr().out

    assert "Series : One Piece" in output
    assert "Chapter: 1" in output
    assert "Title  : Test Chapter" in output
    assert "Arc    : Test Arc" in output
    assert "Status : Inserted" in output


def test_ingestion_cli_rejects_unknown_configuration(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ingest_chapter_metadata",
            "--anime",
            "Unknown Series",
            "--chapter",
            "1",
        ],
    )

    ingest_chapter_metadata.main()

    output = capsys.readouterr().out

    assert (
        'No chapter metadata configuration found '
        'for: "Unknown Series"'
        in output
    )


def test_ingestion_cli_reports_missing_database_anime(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        ingest_chapter_metadata,
        "SessionLocal",
        lambda: FakeSession(),
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "EpisodeRepository",
        FakeRepository,
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ingest_chapter_metadata",
            "--anime",
            "Naruto",
            "--chapter",
            "1",
        ],
    )

    ingest_chapter_metadata.main()

    output = capsys.readouterr().out

    assert (
        'Anime not found in database: "Naruto"'
        in output
    )