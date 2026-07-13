import argparse

import json
from datetime import datetime
from pathlib import Path
from time import perf_counter

from scraper.core.browser_client import BrowserClient
from scraper.database.session import SessionLocal
from scraper.providers.chapter_metadata_factory import (
    create_chapter_metadata_provider,
)
from scraper.repositories.episode_repository import (
    EpisodeRepository,
)
from scraper.services.chapter_metadata_ingestion_service import (
    ChapterMetadataIngestionService,
)
from scraper.services.chapter_url_discovery_service import (
    ChapterUrlDiscoveryService,
)
from scraper.utils.config_loader import load_provider_config


SERIES_CONFIGS = {
    "One Piece": "configs/fandom/one_piece.json",
    "Naruto": "configs/fandom/naruto.json",
}


def chapter_record_is_complete(
    chapter,
) -> bool:
    if chapter is None:
        return False

    return (
        bool(
            chapter.chapter_title
            and chapter.chapter_title.strip()
        )
        and bool(
            chapter.manga_arc
            and chapter.manga_arc.strip()
        )
        and bool(
            chapter.source_url
            and chapter.source_url.strip()
        )
        and chapter.last_updated is not None
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Discover, extract, and save manga chapter metadata."
        )
    )

    parser.add_argument(
        "--anime",
        required=True,
        help="Anime title associated with the manga series.",
    )

    parser.add_argument(
        "--chapter",
        type=int,
        default=None,
        help="Single manga chapter number to ingest.",
    )

    parser.add_argument(
        "--start-chapter",
        type=int,
        default=None,
        help="First chapter number in a controlled range.",
    )

    parser.add_argument(
        "--end-chapter",
        type=int,
        default=None,
        help="Last chapter number in a controlled range.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Preview chapter ingestion without fetching "
            "chapter pages or writing to the database."
        ),
    )

    parser.add_argument(
        "--skip-complete-existing",
        action="store_true",
        help=(
            "Skip existing records that already contain "
            "title, manga arc, source URL, and timestamp."
        ),
    )

    parser.add_argument(
        "--json-report",
        type=str,
        default=None,
        help=(
            "Write an ingestion summary and per-chapter "
            "results to a JSON file."
        ),
    )

    args = parser.parse_args()

    started_at = perf_counter()

    if (
        args.chapter is not None
        and (
            args.start_chapter is not None
            or args.end_chapter is not None
        )
    ):
        print(
            "Use --chapter or a chapter range, "
            "not both."
        )
        return

    if args.chapter is not None:
        chapter_numbers = [
            args.chapter
        ]

    elif (
        args.start_chapter is not None
        and args.end_chapter is not None
    ):
        if args.start_chapter > args.end_chapter:
            print(
                "--start-chapter must be less than or "
                "equal to --end-chapter."
            )
            return

        chapter_numbers = list(
            range(
                args.start_chapter,
                args.end_chapter + 1,
            )
        )

    else:
        print(
            "Provide either --chapter or both "
            "--start-chapter and --end-chapter."
        )
        return

    config_path = SERIES_CONFIGS.get(
        args.anime
    )

    if config_path is None:
        print(
            f'No chapter metadata configuration '
            f'found for: "{args.anime}"'
        )
        return

    session = SessionLocal()

    try:
        repository = EpisodeRepository(
            session
        )

        anime = repository.get_anime_by_title(
            args.anime
        )

        if anime is None:
            print(
                f'Anime not found in database: '
                f'"{args.anime}"'
            )
            return
        
        report = {
            "schema_version": 1,
            "anime": anime.title,
            "start_chapter": chapter_numbers[0],
            "end_chapter": chapter_numbers[-1],
            "chapters_selected": len(chapter_numbers),
            "inserted": 0,
            "updated": 0,
            "skipped": 0,
            "failed": 0,
            "failed_chapters": [],
            "results": [],
            "dry_run": args.dry_run,
            "skip_complete_existing": (
                args.skip_complete_existing
            ),
            "generated_at": None,
            "elapsed_seconds": 0,
            "status": None,
        }

        config = load_provider_config(
            config_path
        )

        browser_client = (
            None
            if args.dry_run
            else BrowserClient()
        )

        discovery_service = (
            ChapterUrlDiscoveryService(
                config=config,
                browser_client=browser_client,
            )
        )

        if args.dry_run:
            existing_count = 0
            insert_count = 0
            update_count = 0
            unresolved_urls = []

            total = len(chapter_numbers)

            print("Chapter Metadata Ingestion Preflight")
            print("------------------------------------")
            print(f"Series            : {anime.title}")
            print(f"Chapters Selected : {total}")
            print("Database Writes    : DISABLED")
            print("Chapter Fetching   : DISABLED")
            print()

            for index, chapter_number in enumerate(
                chapter_numbers,
                start=1,
            ):
                existing = repository.get_chapter_metadata(
                    anime_id=anime.id,
                    chapter_number=chapter_number,
                )

                if existing is None:
                    status = "Would Insert"
                    insert_count += 1
                else:
                    status = "Would Update"
                    existing_count += 1
                    update_count += 1

                source_url = discovery_service.discover_url(
                    chapter_number
                )

                if source_url is None:
                    unresolved_urls.append(
                        chapter_number
                    )

                print(
                    f"[{index}/{total}] "
                    f"Chapter {chapter_number}"
                )
                print(
                    f"  Source: "
                    f"{source_url or 'Not discovered'}"
                )
                print(f"  Status: {status}")
                print()

            print("Preflight Summary")
            print("-----------------")
            print(f"Series            : {anime.title}")
            print(f"Chapters Selected : {total}")
            print(f"Existing Records  : {existing_count}")
            print(f"Would Insert      : {insert_count}")
            print(f"Would Update      : {update_count}")
            print(
                f"Unresolved URLs   : "
                f"{len(unresolved_urls)}"
            )

            if unresolved_urls:
                print("Unresolved Chapters:")

                for chapter_number in unresolved_urls:
                    print(
                        f"  Chapter {chapter_number}"
                    )

            report.update(
                {
                    "would_insert": insert_count,
                    "would_update": update_count,
                    "unresolved_urls": unresolved_urls,
                    "generated_at": (
                        datetime.now().isoformat()
                    ),
                    "elapsed_seconds": round(
                        perf_counter() - started_at,
                        2,
                    ),
                    "status": (
                        "preflight_pass"
                        if not unresolved_urls
                        else "preflight_with_gaps"
                    ),
                }
            )

            if args.json_report:
                Path(args.json_report).write_text(
                    json.dumps(
                        report,
                        indent=2,
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )

                print()
                print(
                    "JSON report written to: "
                    f"{args.json_report}"
                )

            return

            return

        provider = create_chapter_metadata_provider(
            provider_name=anime.provider,
            config_path=config_path,
            browser_client=browser_client,
        )

        ingestion_service = (
            ChapterMetadataIngestionService(
                discovery_service=discovery_service,
                provider=provider,
                repository=repository,
            )
        )

        inserted_count = 0
        updated_count = 0
        failed_chapters = []

        total = len(chapter_numbers)

        print("Chapter Metadata Ingestion")
        print("--------------------------")
        print(f"Series            : {anime.title}")
        print(f"Chapters Selected : {total}")
        print()

        for index, chapter_number in enumerate(
            chapter_numbers,
            start=1,
        ):
            print(
                f"[{index}/{total}] "
                f"Chapter {chapter_number}"
            )

            try:
                existing = repository.get_chapter_metadata(
                    anime_id=anime.id,
                    chapter_number=chapter_number,
                )

                if (
                    args.skip_complete_existing
                    and chapter_record_is_complete(
                        existing
                    )
                ):
                    print("  Status: Skipped (already complete)")
                    print()

                    report["skipped"] += 1
                    report["results"].append(
                        {
                            "chapter_number": chapter_number,
                            "status": "skipped_complete",
                            "chapter_title": (
                                existing.chapter_title
                            ),
                            "manga_arc": (
                                existing.manga_arc
                            ),
                            "source_url": (
                                existing.source_url
                            ),
                            "error": None,
                        }
                    )

                    continue

                chapter = ingestion_service.ingest(
                    anime=anime,
                    chapter_number=chapter_number,
                )

                status = (
                    "Inserted"
                    if existing is None
                    else "Updated"
                )

                if existing is None:
                    inserted_count += 1
                else:
                    updated_count += 1

                print(
                    f"  Title : "
                    f"{chapter.chapter_title or 'Not available'}"
                )
                print(
                    f"  Arc   : "
                    f"{chapter.manga_arc or 'Not available'}"
                )
                print(
                    f"  Source: "
                    f"{chapter.source_url or 'Not available'}"
                )
                if existing is None:
                    report["inserted"] += 1
                else:
                    report["updated"] += 1

                report["results"].append(
                    {
                        "chapter_number": (
                            chapter.chapter_number
                        ),
                        "status": status.lower(),
                        "chapter_title": (
                            chapter.chapter_title
                        ),
                        "manga_arc": chapter.manga_arc,
                        "source_url": (
                            chapter.source_url
                        ),
                        "error": None,
                    }
                )
                print(f"  Status: {status}")
                print()

            except Exception as error:
                failed_chapters.append(
                    {
                        "chapter_number": chapter_number,
                        "error": str(error),
                    }
                )

                print(f"  FAILED: {error}")
                print()

                report["failed"] += 1
                report["failed_chapters"].append(
                    chapter_number
                )
                report["results"].append(
                    {
                        "chapter_number": chapter_number,
                        "status": "failed",
                        "chapter_title": None,
                        "manga_arc": None,
                        "source_url": None,
                        "error": str(error),
                    }
                )

        print("Chapter Metadata Ingestion Summary")
        print("----------------------------------")
        print(f"Series            : {anime.title}")
        print(f"Chapters Selected : {total}")
        print(f"Inserted          : {inserted_count}")
        print(f"Updated           : {updated_count}")
        print(f"Failed            : {len(failed_chapters)}")
        print(f"Skipped           : {report['skipped']}")

        if failed_chapters:
            print("Failed Chapters:")

            for failure in failed_chapters:
                print(
                    f"  Chapter "
                    f"{failure['chapter_number']}: "
                    f"{failure['error']}"
                )

        elapsed_seconds = (
            perf_counter() - started_at
        )

        report.update(
            {
                "generated_at": (
                    datetime.now().isoformat()
                ),
                "elapsed_seconds": round(
                    elapsed_seconds,
                    2,
                ),
                "status": (
                    "completed_with_failures"
                    if report["failed"] > 0
                    else "completed_successfully"
                ),
            }
        )

        if args.json_report:
            Path(args.json_report).write_text(
                json.dumps(
                    report,
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            print()
            print(
                "JSON report written to: "
                f"{args.json_report}"
            )

    except Exception as error:
        print("Chapter metadata ingestion failed.")
        print(f"Reason: {error}")

    finally:
        session.close()


if __name__ == "__main__":
    main()