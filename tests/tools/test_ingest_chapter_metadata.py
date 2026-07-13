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
    

class FakePreflightRepository:
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
        if chapter_number == 1:
            return SimpleNamespace(
                chapter_number=1
            )

        return None
    

class FakePreflightDiscoveryService:
    def __init__(
        self,
        config,
        browser_client=None,
    ):
        self.config = config
        self.browser_client = browser_client

    def discover_url(
        self,
        chapter_number,
    ):
        return (
            "https://example.com/wiki/"
            f"Chapter_{chapter_number}"
        )
    

class PartiallyMissingDiscoveryService:
    def __init__(
        self,
        config,
        browser_client=None,
    ):
        pass

    def discover_url(
        self,
        chapter_number,
    ):
        if chapter_number == 2:
            return None

        return (
            "https://example.com/wiki/"
            f"Chapter_{chapter_number}"
        )
    

def test_ingestion_cli_dry_run_reports_unresolved_urls(
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
        FakePreflightRepository,
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "load_provider_config",
        lambda path: object(),
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "ChapterUrlDiscoveryService",
        PartiallyMissingDiscoveryService,
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "BrowserClient",
        lambda: object(),
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ingest_chapter_metadata",
            "--anime",
            "One Piece",
            "--start-chapter",
            "1",
            "--end-chapter",
            "3",
            "--dry-run",
        ],
    )

    ingest_chapter_metadata.main()

    output = capsys.readouterr().out

    assert "Unresolved URLs   : 1" in output
    assert "Unresolved Chapters:" in output
    assert "Chapter 2" in output


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

    assert "Series            : One Piece" in output
    assert "Chapters Selected : 1" in output
    assert "[1/1] Chapter 1" in output
    assert "Title : Test Chapter" in output
    assert "Arc   : Test Arc" in output
    assert "Status: Inserted" in output
    assert "Inserted          : 1" in output
    assert "Updated           : 0" in output
    assert "Failed            : 0" in output


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

def test_ingestion_cli_rejects_conflicting_selection(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ingest_chapter_metadata",
            "--anime",
            "One Piece",
            "--chapter",
            "1",
            "--start-chapter",
            "1",
            "--end-chapter",
            "5",
        ],
    )

    ingest_chapter_metadata.main()

    output = capsys.readouterr().out

    assert (
        "Use --chapter or a chapter range, not both."
        in output
    )


def test_ingestion_cli_requires_complete_selection(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ingest_chapter_metadata",
            "--anime",
            "One Piece",
            "--start-chapter",
            "1",
        ],
    )

    ingest_chapter_metadata.main()

    output = capsys.readouterr().out

    assert (
        "Provide either --chapter or both "
        "--start-chapter and --end-chapter."
        in output
    )


def test_ingestion_cli_rejects_reversed_range(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ingest_chapter_metadata",
            "--anime",
            "One Piece",
            "--start-chapter",
            "5",
            "--end-chapter",
            "1",
        ],
    )

    ingest_chapter_metadata.main()

    output = capsys.readouterr().out

    assert (
        "--start-chapter must be less than or "
        "equal to --end-chapter."
        in output
    )

def test_ingestion_cli_dry_run_preflight(
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
        FakePreflightRepository,
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "load_provider_config",
        lambda path: object(),
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "ChapterUrlDiscoveryService",
        FakePreflightDiscoveryService,
    )

    def fail_if_browser_created():
        raise AssertionError(
            "BrowserClient should not be created "
            "during dry-run mode."
        )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "BrowserClient",
        fail_if_browser_created,
    )

    def fail_if_provider_created(**kwargs):
        raise AssertionError(
            "Provider should not be created "
            "during dry-run mode."
        )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "create_chapter_metadata_provider",
        fail_if_provider_created,
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ingest_chapter_metadata",
            "--anime",
            "One Piece",
            "--start-chapter",
            "1",
            "--end-chapter",
            "3",
            "--dry-run",
        ],
    )

    ingest_chapter_metadata.main()

    output = capsys.readouterr().out

    assert "Chapter Metadata Ingestion Preflight" in output
    assert "Chapters Selected : 3" in output
    assert "Database Writes    : DISABLED" in output
    assert "Chapter Fetching   : DISABLED" in output
    assert "Existing Records  : 1" in output
    assert "Would Insert      : 2" in output
    assert "Would Update      : 1" in output
    assert "Unresolved URLs   : 0" in output
    assert "[1/3] Chapter 1" in output
    assert "Status: Would Update" in output
    assert "[2/3] Chapter 2" in output
    assert "Status: Would Insert" in output