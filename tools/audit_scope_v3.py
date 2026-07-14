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

from scraper.utils.metadata_exception_loader import (
    get_manga_arc_not_applicable_chapters,
    load_metadata_exceptions,
)


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


def find_missing_chapter_numbers(
    chapter_numbers: list[int],
    expected_start: int,
    expected_end: int,
) -> list[int]:
    existing_numbers = set(
        chapter_numbers
    )

    return [
        chapter_number
        for chapter_number in range(
            expected_start,
            expected_end + 1,
        )
        if chapter_number not in existing_numbers
    ]


def get_exception_path(
    anime_title: str,
) -> Path:
    filename = (
        anime_title
        .strip()
        .lower()
        .replace(" ", "_")
    )

    return Path(
        "configs/exceptions"
    ) / f"{filename}.json"


def load_scope_v3_exceptions(
    anime_title: str,
) -> dict:
    exception_path = get_exception_path(
        anime_title
    )

    if not exception_path.exists():
        return {}

    return load_metadata_exceptions(
        str(exception_path)
    )


def build_scope_v3_report(
    session: Session,
    anime_title: str,
    expected_start: int | None = None,
    expected_end: int | None = None,
    exceptions: dict | None = None,
) -> dict:
    anime = session.execute(
        select(Anime)
        .where(Anime.title == anime_title)
    ).scalar_one_or_none()

    if anime is None:
        raise ValueError(
            f'Anime not found: "{anime_title}"'
        )
    
    if (
        expected_start is None
        and expected_end is not None
    ):
        raise ValueError(
            "Expected start chapter is required "
            "when expected end chapter is provided."
        )

    if (
        expected_start is not None
        and expected_end is None
    ):
        raise ValueError(
            "Expected end chapter is required "
            "when expected start chapter is provided."
        )

    if (
        expected_start is not None
        and expected_end is not None
        and expected_start > expected_end
    ):
        raise ValueError(
            "Expected start chapter must be less than "
            "or equal to expected end chapter."
        )
    
    if exceptions is None:
        exceptions = load_scope_v3_exceptions(
            anime_title
        )

    configured_arc_exceptions = sorted(
        get_manga_arc_not_applicable_chapters(
            exceptions
        )
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

    missing_arc_chapter_set = set(
        missing_arc_chapters
    )

    configured_arc_exception_set = set(
        configured_arc_exceptions
    )

    approved_missing_arc_chapters = sorted(
        missing_arc_chapter_set
        & configured_arc_exception_set
    )

    unresolved_missing_arc_chapters = sorted(
        missing_arc_chapter_set
        - configured_arc_exception_set
    )

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

    existing_chapter_number_set = set(
        chapter_numbers
    )

    unused_arc_exceptions = sorted(
        configured_arc_exception_set
        - missing_arc_chapter_set
    )

    configured_missing_records = sorted(
        configured_arc_exception_set
        - existing_chapter_number_set
    )

    duplicate_chapter_numbers = (
        find_duplicate_chapter_numbers(
            chapter_numbers
        )
    )

    expected_chapter_count = None
    missing_chapter_numbers = []
    coverage_completion = None
    coverage_audit_status = "NOT EVALUATED"

    if (
        expected_start is not None
        and expected_end is not None
    ):
        expected_chapter_count = (
            expected_end
            - expected_start
            + 1
        )

        missing_chapter_numbers = (
            find_missing_chapter_numbers(
                chapter_numbers=chapter_numbers,
                expected_start=expected_start,
                expected_end=expected_end,
            )
        )

        covered_chapter_count = (
            expected_chapter_count
            - len(missing_chapter_numbers)
        )

        coverage_completion = (
            calculate_completion(
                covered_chapter_count,
                expected_chapter_count,
            )
        )

        coverage_audit_status = (
            "PASS"
            if (
                not missing_chapter_numbers
                and not duplicate_chapter_numbers
            )
            else "IN PROGRESS"
        )

    title_complete = (
        chapter_records
        - len(missing_title_chapters)
    )

    arc_complete = (
        chapter_records
        - len(missing_arc_chapters)
    )

    adjusted_arc_complete = (
        chapter_records
        - len(
            unresolved_missing_arc_chapters
        )
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

    adjusted_arc_completion = (
        calculate_completion(
            adjusted_arc_complete,
            chapter_records,
        )
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
        metadata_audit_status = "IN PROGRESS"

    elif (
        title_completion == 100.0
        and adjusted_arc_completion == 100.0
        and source_url_completion == 100.0
        and last_updated_completion == 100.0
        and not duplicate_chapter_numbers
        and not unused_arc_exceptions
        and not configured_missing_records
    ):
        metadata_audit_status = "PASS"

    else:
        metadata_audit_status = "IN PROGRESS"

    if (
        metadata_audit_status == "PASS"
        and coverage_audit_status == "PASS"
    ):
        dataset_status = "PASS"

    else:
        dataset_status = "IN PROGRESS"

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
        "configured_arc_exceptions": (
            configured_arc_exceptions
        ),
        "approved_missing_arcs": len(
            approved_missing_arc_chapters
        ),
        "approved_missing_arc_chapters": (
            approved_missing_arc_chapters
        ),
        "unresolved_missing_arcs": len(
            unresolved_missing_arc_chapters
        ),
        "unresolved_missing_arc_chapters": (
            unresolved_missing_arc_chapters
        ),
        "adjusted_chapters_with_arcs": (
            adjusted_arc_complete
        ),
        "adjusted_arc_completion": (
            adjusted_arc_completion
        ),
        "unused_arc_exceptions": (
            unused_arc_exceptions
        ),
        "configured_missing_arc_records": (
            configured_missing_records
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
        "metadata_audit_status": (
            metadata_audit_status
        ),
        "audit_status": metadata_audit_status,
        "expected_start_chapter": expected_start,
        "expected_end_chapter": expected_end,
        "expected_chapter_count": (
            expected_chapter_count
        ),
        "missing_chapters": len(
            missing_chapter_numbers
        ),
        "missing_chapter_numbers": (
            missing_chapter_numbers
        ),
        "coverage_completion": (
            coverage_completion
        ),
        "coverage_audit_status": (
            coverage_audit_status
        ),
        "dataset_status": dataset_status,
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
        f"Stored Values Complete : "
        f"{report['chapters_with_arcs']}"
    )
    print(
        f"Raw Missing            : "
        f"{report['missing_arcs']}"
    )
    print(
        f"Raw Completion         : "
        f"{report['arc_completion']:.2f}%"
    )
    print(
        f"Approved Not Applicable: "
        f"{report['approved_missing_arcs']}"
    )
    print(
        f"Unresolved Missing     : "
        f"{report['unresolved_missing_arcs']}"
    )
    print(
        f"Adjusted Completion    : "
        f"{report['adjusted_arc_completion']:.2f}%"
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
        f"{report['metadata_audit_status']}"
    )

    print()
    print("Coverage")
    print("--------")

    if (
        report["expected_chapter_count"]
        is None
    ):
        print(
            "Expected Range        : "
            "Not supplied"
        )
        print(
            "Coverage Completion   : "
            "Not evaluated"
        )

    else:
        print(
            f"Expected Range        : "
            f"{report['expected_start_chapter']}"
            f"–{report['expected_end_chapter']}"
        )
        print(
            f"Expected Chapters     : "
            f"{report['expected_chapter_count']}"
        )
        print(
            f"Missing Chapters      : "
            f"{report['missing_chapters']}"
        )
        print(
            f"Coverage Completion   : "
            f"{report['coverage_completion']:.2f}%"
        )

    print(
        f"Coverage Audit Status : "
        f"{report['coverage_audit_status']}"
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
            "Approved Non-Applicable Manga Arcs",
            report[
                "approved_missing_arc_chapters"
            ],
        ),
        (
            "Chapters Missing Manga Arcs",
            report[
                "unresolved_missing_arc_chapters"
            ],
        ),
        (
            "Unused Manga Arc Exceptions",
            report[
                "unused_arc_exceptions"
            ],
        ),
        (
            "Exceptions Without Chapter Records",
            report[
                "configured_missing_arc_records"
            ],
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
        (
            "Missing Chapter Numbers",
            report["missing_chapter_numbers"],
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
        "--expected-start",
        type=int,
        default=None,
        help=(
            "First expected chapter number for "
            "full-range coverage validation."
        ),
    )

    parser.add_argument(
        "--expected-end",
        type=int,
        default=None,
        help=(
            "Last expected chapter number for "
            "full-range coverage validation."
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
                expected_start=args.expected_start,
                expected_end=args.expected_end,
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