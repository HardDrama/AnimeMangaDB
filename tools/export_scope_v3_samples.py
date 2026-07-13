import argparse
import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from scraper.database.models import (
    Anime,
    ChapterMetadata,
)
from scraper.database.session import SessionLocal


def parse_chapter_numbers(
    value: str,
) -> list[int]:
    chapter_numbers = []

    for item in value.split(","):
        item = item.strip()

        if not item:
            continue

        try:
            chapter_number = int(item)
        except ValueError as error:
            raise ValueError(
                f'Invalid chapter number: "{item}"'
            ) from error

        if chapter_number <= 0:
            raise ValueError(
                "Chapter numbers must be positive integers."
            )

        chapter_numbers.append(
            chapter_number
        )

    if not chapter_numbers:
        raise ValueError(
            "At least one chapter number is required."
        )

    return sorted(
        set(chapter_numbers)
    )


def build_sample_report(
    session: Session,
    anime_title: str,
    chapter_numbers: list[int],
) -> dict:
    anime = session.execute(
        select(Anime)
        .where(Anime.title == anime_title)
    ).scalar_one_or_none()

    if anime is None:
        raise ValueError(
            f'Anime not found: "{anime_title}"'
        )

    chapters = session.execute(
        select(ChapterMetadata)
        .where(
            ChapterMetadata.anime_id == anime.id
        )
        .where(
            ChapterMetadata.chapter_number.in_(
                chapter_numbers
            )
        )
        .order_by(
            ChapterMetadata.chapter_number
        )
    ).scalars().all()

    chapters_by_number = {
        chapter.chapter_number: chapter
        for chapter in chapters
    }

    results = []
    missing_records = []

    for chapter_number in chapter_numbers:
        chapter = chapters_by_number.get(
            chapter_number
        )

        if chapter is None:
            missing_records.append(
                chapter_number
            )

            results.append(
                {
                    "chapter_number": chapter_number,
                    "record_found": False,
                    "chapter_title": None,
                    "manga_arc": None,
                    "source_url": None,
                    "last_updated": None,
                    "manual_title_match": None,
                    "manual_arc_match": None,
                    "manual_url_valid": None,
                    "manual_notes": None,
                }
            )

            continue

        results.append(
            {
                "chapter_number": chapter.chapter_number,
                "record_found": True,
                "chapter_title": chapter.chapter_title,
                "manga_arc": chapter.manga_arc,
                "source_url": chapter.source_url,
                "last_updated": (
                    chapter.last_updated.isoformat()
                    if chapter.last_updated is not None
                    else None
                ),
                "manual_title_match": None,
                "manual_arc_match": None,
                "manual_url_valid": None,
                "manual_notes": None,
            }
        )

    return {
        "schema_version": 1,
        "anime": anime.title,
        "anime_id": anime.id,
        "chapters_requested": len(
            chapter_numbers
        ),
        "records_found": (
            len(chapter_numbers)
            - len(missing_records)
        ),
        "missing_records": len(
            missing_records
        ),
        "missing_chapter_numbers": (
            missing_records
        ),
        "generated_at": datetime.now().isoformat(),
        "validation_status": "PENDING MANUAL REVIEW",
        "results": results,
    }


def print_sample_report(
    report: dict,
) -> None:
    print("Scope v3 Manual Validation Samples")
    print("----------------------------------")
    print(f"Anime              : {report['anime']}")
    print(
        f"Chapters Requested : "
        f"{report['chapters_requested']}"
    )
    print(
        f"Records Found      : "
        f"{report['records_found']}"
    )
    print(
        f"Missing Records    : "
        f"{report['missing_records']}"
    )
    print()

    for result in report["results"]:
        print(
            f"Chapter {result['chapter_number']}"
        )
        print(
            f"  Record : "
            f"{'Found' if result['record_found'] else 'Missing'}"
        )

        if result["record_found"]:
            print(
                f"  Title  : "
                f"{result['chapter_title']}"
            )
            print(
                f"  Arc    : "
                f"{result['manga_arc']}"
            )
            print(
                f"  Source : "
                f"{result['source_url']}"
            )

        print()


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Export selected Scope v3 chapter records "
            "for representative manual validation."
        )
    )

    parser.add_argument(
        "--anime",
        required=True,
        help="Anime title to review.",
    )

    parser.add_argument(
        "--chapters",
        required=True,
        help=(
            "Comma-separated chapter numbers, "
            'for example: "1,50,100,1188".'
        ),
    )

    parser.add_argument(
        "--json-report",
        type=str,
        default=None,
        help=(
            "Write the manual validation manifest "
            "to a JSON file."
        ),
    )

    args = parser.parse_args()

    try:
        chapter_numbers = parse_chapter_numbers(
            args.chapters
        )
    except ValueError as error:
        print(error)
        return

    session = SessionLocal()

    try:
        try:
            report = build_sample_report(
                session=session,
                anime_title=args.anime,
                chapter_numbers=chapter_numbers,
            )
        except ValueError as error:
            print(error)
            return

        print_sample_report(
            report
        )

        if args.json_report:
            report_path = Path(
                args.json_report
            )

            report_path.write_text(
                json.dumps(
                    report,
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            print(
                "Manual validation manifest written to: "
                f"{report_path}"
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()