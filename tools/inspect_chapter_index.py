import argparse
import json
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup

from scraper.core.browser_client import BrowserClient
from scraper.services.chapter_url_discovery_service import (
    ChapterUrlDiscoveryService,
)
from scraper.utils.config_loader import load_provider_config


def extract_numbered_entries(
    container,
) -> list[dict]:
    entries = []

    for list_item in container.select(
        "li"
    ):
        text = " ".join(
            list_item.get_text(
                " ",
                strip=True,
            ).split()
        )

        chapter_number = (
            ChapterUrlDiscoveryService
            ._extract_numbered_list_item(
                text
            )
        )

        if chapter_number is None:
            continue

        link = list_item.find(
            "a",
            href=True,
        )

        if link is None:
            continue

        entries.append(
            {
                "chapter_number": chapter_number,
                "title": " ".join(
                    link.get_text(
                        " ",
                        strip=True,
                    ).split()
                ),
                "href": link["href"],
            }
        )

    return entries

def inspect_numbered_section(
    html: str,
    section_id: str,
    subsection_ids: list[str] | None = None,
) -> dict:
    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    heading_marker = soup.find(
        id=section_id
    )

    if heading_marker is None:
        raise ValueError(
            f'Index section not found: "{section_id}"'
        )

    heading = heading_marker.find_parent(
        "h2"
    )

    if heading is None:
        raise ValueError(
            f'Section "{section_id}" is not inside an h2.'
        )

    chapter_entries = []

    configured_subsections = (
        subsection_ids
        or []
    )

    if configured_subsections:
        for subsection_id in configured_subsections:
            subsection_marker = soup.find(
                id=subsection_id
            )

            if subsection_marker is None:
                raise ValueError(
                    "Index subsection not found: "
                    f'"{subsection_id}"'
                )

            subsection_heading = (
                subsection_marker.find_parent(
                    ["h3", "h4"]
                )
            )

            if subsection_heading is None:
                raise ValueError(
                    f'Subsection "{subsection_id}" '
                    "is not inside an h3 or h4."
                )

            for sibling in (
                subsection_heading.find_next_siblings()
            ):
                if sibling.name in {
                    "h2",
                    "h3",
                }:
                    break

                chapter_entries.extend(
                    extract_numbered_entries(
                        sibling
                    )
                )

    else:
        for sibling in heading.find_next_siblings():
            if sibling.name == "h2":
                break

            chapter_entries.extend(
                extract_numbered_entries(
                    sibling
                )
            )

    chapter_numbers = [
        entry["chapter_number"]
        for entry in chapter_entries
    ]

    unique_chapter_numbers = sorted(
        set(chapter_numbers)
    )

    duplicate_chapter_numbers = sorted(
        {
            chapter_number
            for chapter_number in chapter_numbers
            if chapter_numbers.count(
                chapter_number
            ) > 1
        }
    )

    if unique_chapter_numbers:
        minimum_chapter = min(
            unique_chapter_numbers
        )
        maximum_chapter = max(
            unique_chapter_numbers
        )
    else:
        minimum_chapter = None
        maximum_chapter = None

    missing_chapter_numbers = []

    if (
        minimum_chapter is not None
        and maximum_chapter is not None
    ):
        present = set(
            unique_chapter_numbers
        )

        missing_chapter_numbers = [
            chapter_number
            for chapter_number in range(
                minimum_chapter,
                maximum_chapter + 1,
            )
            if chapter_number not in present
        ]

    return {
        "section_id": section_id,
        "entry_count": len(
            chapter_entries
        ),
        "unique_chapter_count": len(
            unique_chapter_numbers
        ),
        "minimum_chapter": minimum_chapter,
        "maximum_chapter": maximum_chapter,
        "missing_chapter_count": len(
            missing_chapter_numbers
        ),
        "missing_chapter_numbers": (
            missing_chapter_numbers
        ),
        "duplicate_chapter_count": len(
            duplicate_chapter_numbers
        ),
        "duplicate_chapter_numbers": (
            duplicate_chapter_numbers
        ),
        "entries": chapter_entries,
    }


def print_report(
    report: dict,
) -> None:
    print("Chapter Index Inspection")
    print("------------------------")
    print(
        f"Anime                 : "
        f"{report['anime']}"
    )
    print(
        f"Index URL             : "
        f"{report['index_url']}"
    )
    print(
        f"Section ID            : "
        f"{report['section_id']}"
    )
    print(
        f"Entries Found         : "
        f"{report['entry_count']}"
    )
    print(
        f"Unique Chapters       : "
        f"{report['unique_chapter_count']}"
    )
    print(
        f"Minimum Chapter       : "
        f"{report['minimum_chapter']}"
    )
    print(
        f"Maximum Chapter       : "
        f"{report['maximum_chapter']}"
    )
    print(
        f"Missing Chapters      : "
        f"{report['missing_chapter_count']}"
    )
    print(
        f"Duplicate Chapters    : "
        f"{report['duplicate_chapter_count']}"
    )
    print(
        f"Inspection Status     : "
        f"{report['inspection_status']}"
    )

    if report["missing_chapter_numbers"]:
        print()
        print("Missing Chapter Numbers")
        print("-----------------------")

        for chapter_number in (
            report["missing_chapter_numbers"]
        ):
            print(
                f"Chapter {chapter_number}"
            )

    if report["duplicate_chapter_numbers"]:
        print()
        print("Duplicate Chapter Numbers")
        print("-------------------------")

        for chapter_number in (
            report["duplicate_chapter_numbers"]
        ):
            print(
                f"Chapter {chapter_number}"
            )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Inspect a configured numbered chapter-index "
            "section without ingesting chapter pages."
        )
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Provider configuration path.",
    )

    parser.add_argument(
        "--html-file",
        default=None,
        help=(
            "Optional saved index HTML. When omitted, "
            "the configured live index is fetched."
        ),
    )

    parser.add_argument(
        "--json-report",
        default=None,
        help="Write the inspection report to JSON.",
    )

    args = parser.parse_args()

    config = load_provider_config(
        args.config
    )

    chapter_config = config.chapter_metadata

    if chapter_config is None:
        print(
            "Chapter metadata configuration is missing."
        )
        return

    if chapter_config.index_section_id is None:
        print(
            "Chapter index section ID is missing."
        )
        return

    if args.html_file:
        html = Path(
            args.html_file
        ).read_text(
            encoding="utf-8"
        )
    else:
        browser_client = BrowserClient()

        index_url = (
            config.base_url
            + chapter_config.index_path
        )

        html = browser_client.fetch(
            index_url
        )

    index_url = (
        config.base_url
        + chapter_config.index_path
    )

    try:
        section_report = inspect_numbered_section(
            html=html,
            section_id=(
                chapter_config.index_section_id
            ),
            subsection_ids=(
                chapter_config.index_subsection_ids
            ),
        )

    except ValueError as error:
        print(error)
        return

    inspection_status = (
        "PASS"
        if (
            section_report[
                "minimum_chapter"
            ] == 1
            and section_report[
                "maximum_chapter"
            ] == 700
            and section_report[
                "unique_chapter_count"
            ] == 700
            and section_report[
                "missing_chapter_count"
            ] == 0
            and section_report[
                "duplicate_chapter_count"
            ] == 0
        )
        else "REVIEW REQUIRED"
    )

    report = {
        "schema_version": 1,
        "anime": config.series,
        "index_url": index_url,
        **section_report,
        "subsection_ids": (
            chapter_config.index_subsection_ids
            or []
        ),
        "inspection_status": (
            inspection_status
        ),
        "generated_at": (
            datetime.now().isoformat()
        ),
    }

    print_report(
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
            "Inspection report written to: "
            f"{report_path}"
        )
        print(
            f"Subsections           : "
            f"{', '.join(report['subsection_ids']) or 'None'}"
        )


if __name__ == "__main__":
    main()