import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from scraper.database.models import (
    Anime,
    ChapterMetadata,
)
from scraper.database.session import SessionLocal


def calculate_completion(
    complete_count: int,
    total_count: int,
) -> float:
    if total_count == 0:
        return 0.0

    return round(
        complete_count / total_count * 100,
        2,
    )


def find_duplicate_chapter_numbers(
    chapter_numbers: list[int],
) -> list[int]:
    counts = Counter(
        chapter_numbers
    )

    return sorted(
        chapter_number
        for chapter_number, count in counts.items()
        if count > 1
    )


def build_scope_v3_report(
    session: Session,
    anime_title: str,
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
        .order_by(
            ChapterMetadata.chapter_number
        )
    ).scalars().all()

    chapter_records = len(chapters)

    missing_title_chapters = [
        chapter.chapter_number
        for chapter in chapters
        if (
            chapter.chapter_title is None
            or not chapter.chapter_title.strip()
        )
    ]

    missing_arc_chapters = [
        chapter.chapter_number
        for chapter in chapters
        if (
            chapter.manga_arc is None
            or not chapter.manga_arc.strip()
        )
    ]

    missing_source_url_chapters = [
        chapter.chapter_number
        for chapter in chapters
        if (
            chapter.source_url is None
            or not chapter.source_url.strip()
        )
    ]

    missing_last_updated_chapters = [
        chapter.chapter_number
        for chapter in chapters
        if chapter.last_updated is None
    ]

    chapter_numbers = [
        chapter.chapter_number
        for chapter in chapters
    ]

    duplicate_chapter_numbers = (
        find_duplicate_chapter_numbers(
            chapter_numbers
        )
    )

    title_complete = (
        chapter_records
        - len(missing_title_chapters)
    )

    arc_complete = (
        chapter_records
        - len(missing_arc_chapters)
    )

    source_url_complete = (
        chapter_records
        - len(missing_source_url_chapters)
    )

    last_updated_complete = (
        chapter_records
        - len(missing_last_updated_chapters)
    )

    title_completion = calculate_completion(
        title_complete,
        chapter_records,
    )

    arc_completion = calculate_completion(
        arc_complete,
        chapter_records,
    )

    source_url_completion = calculate_completion(
        source_url_complete,
        chapter_records,
    )

    last_updated_completion = calculate_completion(
        last_updated_complete,
        chapter_records,
    )

    if chapter_records == 0:
        audit_status = "IN PROGRESS"

    elif (
        title_completion == 100.0
        and arc_completion == 100.0
        and source_url_completion == 100.0
        and last_updated_completion == 100.0
        and not duplicate_chapter_numbers
    ):
        audit_status = "PASS"

    else:
        audit_status = "IN PROGRESS"

    return {
        "schema_version": 1,
        "anime": anime.title,
        "anime_id": anime.id,
        "chapter_records": chapter_records,
        "chapters_with_titles": title_complete,
        "missing_titles": len(
            missing_title_chapters
        ),
        "title_completion": title_completion,
        "chapters_with_arcs": arc_complete,
        "missing_arcs": len(
            missing_arc_chapters
        ),
        "arc_completion": arc_completion,
        "chapters_with_source_urls": (
            source_url_complete
        ),
        "missing_source_urls": len(
            missing_source_url_chapters
        ),
        "source_url_completion": (
            source_url_completion
        ),
        "chapters_with_last_updated": (
            last_updated_complete
        ),
        "missing_last_updated": len(
            missing_last_updated_chapters
        ),
        "last_updated_completion": (
            last_updated_completion
        ),
        "duplicate_chapters": len(
            duplicate_chapter_numbers
        ),
        "duplicate_chapter_numbers": (
            duplicate_chapter_numbers
        ),
        "missing_title_chapters": (
            missing_title_chapters
        ),
        "missing_arc_chapters": (
            missing_arc_chapters
        ),
        "missing_source_url_chapters": (
            missing_source_url_chapters
        ),
        "missing_last_updated_chapters": (
            missing_last_updated_chapters
        ),
        "audit_status": audit_status,
        "dataset_status": "IN PROGRESS",
        "generated_at": datetime.now().isoformat(),
    }


def print_scope_v3_report(
    report: dict,
) -> None:
    print("Scope v3 Chapter Metadata Audit")
    print("-------------------------------")
    print()
    print(f"Anime                 : {report['anime']}")
    print(
        f"Chapter Records       : "
        f"{report['chapter_records']}"
    )
    print()
    print("Chapter Titles")
    print("--------------")
    print(
        f"Complete              : "
        f"{report['chapters_with_titles']}"
    )
    print(
        f"Missing               : "
        f"{report['missing_titles']}"
    )
    print(
        f"Completion            : "
        f"{report['title_completion']:.2f}%"
    )
    print()
    print("Manga Arcs")
    print("----------")
    print(
        f"Complete              : "
        f"{report['chapters_with_arcs']}"
    )
    print(
        f"Missing               : "
        f"{report['missing_arcs']}"
    )
    print(
        f"Completion            : "
        f"{report['arc_completion']:.2f}%"
    )
    print()
    print("Source URLs")
    print("-----------")
    print(
        f"Complete              : "
        f"{report['chapters_with_source_urls']}"
    )
    print(
        f"Missing               : "
        f"{report['missing_source_urls']}"
    )
    print(
        f"Completion            : "
        f"{report['source_url_completion']:.2f}%"
    )
    print()
    print("Last Updated")
    print("------------")
    print(
        f"Complete              : "
        f"{report['chapters_with_last_updated']}"
    )
    print(
        f"Missing               : "
        f"{report['missing_last_updated']}"
    )
    print(
        f"Completion            : "
        f"{report['last_updated_completion']:.2f}%"
    )
    print()
    print(
        f"Duplicate Chapters    : "
        f"{report['duplicate_chapters']}"
    )
    print()
    print(
        f"Metadata Audit Status : "
        f"{report['audit_status']}"
    )
    print(
        f"Dataset Status        : "
        f"{report['dataset_status']}"
    )

    detail_sections = [
        (
            "Chapters Missing Titles",
            report["missing_title_chapters"],
        ),
        (
            "Chapters Missing Manga Arcs",
            report["missing_arc_chapters"],
        ),
        (
            "Chapters Missing Source URLs",
            report["missing_source_url_chapters"],
        ),
        (
            "Chapters Missing Last Updated",
            report["missing_last_updated_chapters"],
        ),
        (
            "Duplicate Chapter Numbers",
            report["duplicate_chapter_numbers"],
        ),
    ]

    for heading, chapter_numbers in detail_sections:
        if not chapter_numbers:
            continue

        print()
        print(heading)
        print("-" * len(heading))

        for chapter_number in chapter_numbers:
            print(
                f"Chapter {chapter_number}"
            )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Audit Scope v3 manga chapter metadata."
        )
    )

    parser.add_argument(
        "--anime",
        type=str,
        default="One Piece",
        help=(
            "Anime title whose chapter metadata "
            "should be audited. Defaults to One Piece."
        ),
    )

    parser.add_argument(
        "--json-report",
        type=str,
        default=None,
        help="Write the audit report to a JSON file.",
    )

    args = parser.parse_args()

    session = SessionLocal()

    try:
        try:
            report = build_scope_v3_report(
                session=session,
                anime_title=args.anime,
            )

        except ValueError as error:
            print(error)
            return

        print_scope_v3_report(
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

            print()
            print(
                f"Audit report written to: "
                f"{report_path}"
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()