"""
Inspect stored Boruto episode fixtures before characterization values are added.

Run from the repository root:

    python scripts/inspect_boruto_fixtures.py
"""

from __future__ import annotations

from copy import copy
from pathlib import Path
import json
import re
from typing import Any

from bs4 import BeautifulSoup, Tag


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = PROJECT_ROOT / "tests" / "fixtures" / "boruto" / "episodes"
REPORT_PATH = PROJECT_ROOT / "reports" / "boruto_fixture_observation.json"

BENCHMARK_EPISODES = (
    1, 19, 39, 53, 65, 148, 181, 189, 192, 220, 287, 293,
)

CANDIDATE_SELECTORS = {
    "infobox": (
        "aside.portable-infobox",
        "aside.portable-infobox.type-episode",
    ),
    "title": (
        "h2.pi-title",
        "aside.portable-infobox h2.pi-title",
    ),
    "chapter": (
        'div[data-source="chapters"]',
        'div[data-source="chapter"]',
        'div[data-source="manga"]',
    ),
    "arc": (
        'div[data-source="arc"]',
        'div[data-source="arcs"]',
    ),
}


def fixture_path(episode_number: int) -> Path:
    return FIXTURE_ROOT / f"episode_{episode_number:03d}.html"


def normalize_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\s+,", ",", value)
    return re.sub(r",\s*", ", ", value)


def clean_title_text(title_element: Tag | None) -> str | None:
    if title_element is None:
        return None

    cleaned = copy(title_element)

    for control in cleaned.select(
        'a[href*="Special:FormEdit"], '
        'a[title*="edit" i], '
        'span[style*="float:right"]'
    ):
        control.decompose()

    return normalize_text(
        cleaned.get_text(" ", strip=True)
    ).strip('"“”')


def field_value_text(field: Tag | None) -> str | None:
    if field is None:
        return None

    value = field.select_one(".pi-data-value")

    if value is not None:
        return normalize_text(value.get_text(" ", strip=True))

    return normalize_text(field.get_text(" ", strip=True))


def first_match(
    soup: BeautifulSoup,
    selectors: tuple[str, ...],
) -> tuple[str | None, Tag | None]:
    for selector in selectors:
        element = soup.select_one(selector)

        if element is not None:
            return selector, element

    return None, None


def data_source_inventory(infobox: Tag | None) -> list[dict[str, str]]:
    if infobox is None:
        return []

    inventory = []

    for element in infobox.select("[data-source]"):
        source = element.get("data-source")

        if not isinstance(source, str):
            continue

        label = element.select_one(".pi-data-label")
        value = element.select_one(".pi-data-value")

        inventory.append(
            {
                "data_source": source,
                "label": (
                    normalize_text(label.get_text(" ", strip=True))
                    if label is not None
                    else ""
                ),
                "value": (
                    normalize_text(value.get_text(" ", strip=True))
                    if value is not None
                    else normalize_text(element.get_text(" ", strip=True))
                ),
            }
        )

    return inventory


def inspect_episode(episode_number: int) -> dict[str, Any]:
    path = fixture_path(episode_number)

    if not path.is_file():
        raise FileNotFoundError(f"Missing fixture: {path}")

    html = path.read_text(encoding="utf-8")

    if not html.strip():
        raise ValueError(f"Fixture is empty: {path}")

    soup = BeautifulSoup(html, "html.parser")

    infobox_selector, infobox = first_match(
        soup, CANDIDATE_SELECTORS["infobox"]
    )
    title_selector, title = first_match(
        soup, CANDIDATE_SELECTORS["title"]
    )
    chapter_selector, chapter = first_match(
        soup, CANDIDATE_SELECTORS["chapter"]
    )
    arc_selector, arc = first_match(
        soup, CANDIDATE_SELECTORS["arc"]
    )

    return {
        "episode_number": episode_number,
        "fixture": path.name,
        "selectors": {
            "infobox": infobox_selector,
            "title": title_selector,
            "chapter": chapter_selector,
            "arc": arc_selector,
        },
        "values": {
            "title": clean_title_text(title),
            "chapter": field_value_text(chapter),
            "arc": field_value_text(arc),
        },
        "infobox_classes": (
            list(infobox.get("class", []))
            if infobox is not None
            else []
        ),
        "data_sources": data_source_inventory(infobox),
    }


def print_observation(record: dict[str, Any]) -> None:
    print("=" * 80)
    print(f"Episode {record['episode_number']:03d}")
    print(f"Fixture: {record['fixture']}")
    print(f"Selectors: {record['selectors']}")
    print(f"Values: {record['values']}")
    print("data-source fields:")

    for field in record["data_sources"]:
        print(
            f"  - {field['data_source']!r}: "
            f"{field['label']!r} -> {field['value']!r}"
        )


def main() -> int:
    records = [
        inspect_episode(episode_number)
        for episode_number in BENCHMARK_EPISODES
    ]

    for record in records:
        print_observation(record)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "benchmark_name": "Boruto",
        "source_provider": "Fandom",
        "source_type": "Episode",
        "episodes": records,
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("=" * 80)
    print(f"Observation report written to: {REPORT_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
