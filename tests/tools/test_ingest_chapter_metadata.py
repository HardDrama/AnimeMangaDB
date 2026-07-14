import sys
from types import SimpleNamespace

from tools import ingest_chapter_metadata

import json
from datetime import datetime


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
    

class NarutoPreflightRepository:
    anime = SimpleNamespace(
        id=2,
        title="Naruto",
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
        if title == "Naruto":
            return self.anime

        return None

    def get_chapter_metadata(
        self,
        anime_id,
        chapter_number,
    ):
        if chapter_number in {
            1,
            2,
            3,
            4,
            5,
        }:
            return SimpleNamespace(
                chapter_number=chapter_number
            )

        return None
    

class FakeIndexBrowser:
    instances_created = 0

    def __init__(self):
        self.__class__.instances_created += 1
    

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
    

class FakeNarutoPreflightDiscoveryService:
    browser_client_received = None

    def __init__(
        self,
        config,
        browser_client=None,
    ):
        self.__class__.browser_client_received = (
            browser_client
        )

    def discover_url(
        self,
        chapter_number,
    ):
        return (
            "https://naruto.fandom.com/wiki/"
            f"Test_Chapter_{chapter_number}"
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
    

class SkipCompleteRepository:
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
            return CompleteChapterRecord()

        return None
    

class TrackingIngestionService:
    calls = []

    def __init__(
        self,
        discovery_service,
        provider,
        repository,
    ):
        self.repository = repository

    def ingest(
        self,
        anime,
        chapter_number,
    ):
        self.__class__.calls.append(
            chapter_number
        )

        return SimpleNamespace(
            chapter_number=chapter_number,
            chapter_title="New Chapter",
            manga_arc="New Arc",
            source_url=(
                "https://example.com/chapter/"
                f"{chapter_number}"
            ),
        )
    

def test_ingestion_cli_skips_complete_existing_record(
    monkeypatch,
    capsys,
):
    TrackingIngestionService.calls = []

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "SessionLocal",
        lambda: FakeSession(),
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "EpisodeRepository",
        SkipCompleteRepository,
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
        TrackingIngestionService,
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
            "2",
            "--skip-complete-existing",
        ],
    )

    ingest_chapter_metadata.main()

    output = capsys.readouterr().out

    assert (
        "Status: Skipped (already complete)"
        in output
    )
    assert "Skipped           : 1" in output

    assert TrackingIngestionService.calls == [
        2
    ]


def test_ingestion_cli_writes_json_report(
    monkeypatch,
    tmp_path,
    capsys,
):
    configure_successful_ingestion(
        monkeypatch
    )

    report_path = (
        tmp_path
        / "chapter_ingestion_report.json"
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
            "--json-report",
            str(report_path),
        ],
    )

    ingest_chapter_metadata.main()

    output = capsys.readouterr().out

    assert report_path.exists()
    assert (
        "JSON report written to:"
        in output
    )

    report = json.loads(
        report_path.read_text(
            encoding="utf-8"
        )
    )

    assert report["anime"] == "One Piece"
    assert report["chapters_selected"] == 1
    assert report["inserted"] == 1
    assert report["updated"] == 0
    assert report["skipped"] == 0
    assert report["failed"] == 0
    assert (
        report["status"]
        == "completed_successfully"
    )

    assert len(
        report["results"]
    ) == 1

    assert (
        report["results"][0]["chapter_number"]
        == 1
    )

    assert (
        report["results"][0]["status"]
        == "inserted"
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

class CompleteChapterRecord:
    chapter_number = 1
    chapter_title = "Existing Chapter"
    manga_arc = "Existing Arc"
    source_url = "https://example.com/chapter/1"
    last_updated = datetime.now()

def test_complete_chapter_record_detection():
    assert (
        ingest_chapter_metadata
        .chapter_record_is_complete(
            CompleteChapterRecord()
        )
    )

    incomplete = SimpleNamespace(
        chapter_title=None,
        manga_arc="Arc",
        source_url="https://example.com",
        last_updated=datetime.now(),
    )

    assert not (
        ingest_chapter_metadata
        .chapter_record_is_complete(
            incomplete
        )
    )

def test_dry_run_browser_requirement():
    numbered_config = SimpleNamespace(
        chapter_metadata=SimpleNamespace(
            url_strategy="numbered"
        )
    )

    discovered_config = SimpleNamespace(
        chapter_metadata=SimpleNamespace(
            url_strategy="discovered_links"
        )
    )

    numbered_list_config = SimpleNamespace(
        chapter_metadata=SimpleNamespace(
            url_strategy="numbered_list_items"
        )
    )

    assert not (
        ingest_chapter_metadata
        .dry_run_requires_browser(
            numbered_config
        )
    )

    assert (
        ingest_chapter_metadata
        .dry_run_requires_browser(
            discovered_config
        )
    )

    assert (
        ingest_chapter_metadata
        .dry_run_requires_browser(
            numbered_list_config
        )
    )

def test_naruto_dry_run_uses_index_browser(
    monkeypatch,
    capsys,
):
    FakeIndexBrowser.instances_created = 0

    (
        FakeNarutoPreflightDiscoveryService
        .browser_client_received
    ) = None

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "SessionLocal",
        lambda: FakeSession(),
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "EpisodeRepository",
        NarutoPreflightRepository,
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "load_provider_config",
        lambda path: SimpleNamespace(
            chapter_metadata=SimpleNamespace(
                url_strategy=(
                    "numbered_list_items"
                )
            )
        ),
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "BrowserClient",
        FakeIndexBrowser,
    )

    monkeypatch.setattr(
        ingest_chapter_metadata,
        "ChapterUrlDiscoveryService",
        FakeNarutoPreflightDiscoveryService,
    )

    def fail_if_provider_created(
        **kwargs,
    ):
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
            "Naruto",
            "--start-chapter",
            "1",
            "--end-chapter",
            "7",
            "--dry-run",
        ],
    )

    ingest_chapter_metadata.main()

    output = capsys.readouterr().out

    assert FakeIndexBrowser.instances_created == 1

    assert (
        FakeNarutoPreflightDiscoveryService
        .browser_client_received
        is not None
    )

    assert "Series            : Naruto" in output
    assert "Chapters Selected : 7" in output
    assert "Existing Records  : 5" in output
    assert "Would Insert      : 2" in output
    assert "Would Update      : 5" in output
    assert "Unresolved URLs   : 0" in output
    assert "Chapter Fetching   : DISABLED" in output
    assert "Index Fetching       : ENABLED" in output