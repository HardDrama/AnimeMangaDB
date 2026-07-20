"""
Naruto Shippuden source-page characterization tests.

These tests preserve the observed structure and metadata values of the
Naruto Shippuden benchmark episode pages before production implementation.

The tests intentionally inspect stored HTML fixtures directly. They do not
call production providers, extractors, repositories, APIs, or database code.

Naruto Shippuden reuses the existing certified Naruto manga dataset, so this
benchmark stores episode fixtures only.
"""

from copy import copy
from pathlib import Path
import re

import pytest
from bs4 import BeautifulSoup, Tag


# ============================================================================
# Fixture locations and benchmark scope
# ============================================================================

FIXTURE_ROOT = (
    Path(__file__).parent
    / "fixtures"
    / "naruto_shippuden"
    / "episodes"
)

# ============================================================================
# Benchmark metadata
# ============================================================================

BENCHMARK_NAME = "Naruto Shippuden"

SOURCE_PROVIDER = "Fandom"

SOURCE_TYPE = "Episode"

BENCHMARK_VERSION = "v0.63.5"

BENCHMARK_EPISODES = (
    1,
    20,
    68,
    81,
    101,
    102,
    107,
    136,
    142,
    148,
    158,
)


# ============================================================================
# Shared selectors
# ============================================================================

DEFAULT_SELECTORS = {
    "infobox": "aside.portable-infobox.type-episode",
    "title": "h2.pi-title",
    "chapter": 'div[data-source="chapters"]',
    "chapter_value": 'div[data-source="chapters"] .pi-data-value',
    "arc": 'div[data-source="arc"]',
    "arc_value": 'div[data-source="arc"] .pi-data-value',
}


# ============================================================================
# Benchmark expectations
# ============================================================================

EXPECTED_EPISODES = {
    1: {
        "classification": "arc_start",
        "mapping_shape": "single",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Homecoming",
        "expected_chapter_text": "Naruto Chapter #245",
        "expected_arc": "Kazekage Rescue Mission",
        "notes": "First Naruto Shippuden episode.",
    },
    20: {
        "classification": "arc_start",
        "mapping_shape": "multiple",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Hiruko vs. Two Kunoichi!",
        "expected_chapter_text": "Naruto Chapter #264, Naruto Chapter #265",
        "expected_arc": "Kazekage Rescue Mission",
        "notes": "Start of benchmark arc.",
    },
    68: {
        "classification": "arc_start",
        "mapping_shape": "none",
        "expects_chapter_mapping": False,
        "expects_arc": True,
        "expected_title": "Moment of Awakening",
        "expected_chapter_text": "",
        "expected_arc": "Twelve Guardian Ninja",
        "notes": "Start of benchmark arc. No manga chapter mapping.",
    },
    81: {
        "classification": "arc_start",
        "mapping_shape": "multiple",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Sad News",
        "expected_chapter_text": "Naruto Chapter #329, Naruto Chapter #330",
        "expected_arc": "Akatsuki Suppression Mission",
        "notes": "Start of benchmark arc.",
    },
    101: {
        "classification": "arc_start",
        "mapping_shape": "none",
        "expects_chapter_mapping": False,
        "expects_arc": True,
        "expected_title": "Everyone's Feelings",
        "expected_chapter_text": "",
        "expected_arc": "Three-Tails' Appearance",
        "notes": "Start of benchmark arc. No manga chapter mapping.",
    },
    102: {
        "classification": "arc_start",
        "mapping_shape": "none",
        "expects_chapter_mapping": False,
        "expects_arc": True,
        "expected_title": "Regroup!",
        "expected_chapter_text": "",
        "expected_arc": "Three-Tails' Appearance",
        "notes": "Start of benchmark arc. No manga chapter mapping.",
    },
    107: {
        "classification": "arc_start",
        "mapping_shape": "none",
        "expects_chapter_mapping": False,
        "expects_arc": True,
        "expected_title": "Strange Bedfellows",
        "expected_chapter_text": "",
        "expected_arc": "Three-Tails' Appearance",
        "notes": "Start of benchmark arc. No manga chapter mapping.",
    },
    136: {
        "classification": "arc_start",
        "mapping_shape": "multiple",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "The Light and Dark of the Mangekyō Sharingan",
        "expected_chapter_text": "Naruto Chapter #386, Naruto Chapter #387",
        "expected_arc": "Fated Battle Between Brothers",
        "notes": "Start of benchmark arc.",
    },
    142: {
        "classification": "arc_start",
        "mapping_shape": "multiple",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Battle of Valley of Clouds and Lightning",
        "expected_chapter_text": (
            "Naruto Chapter #403, Naruto Chapter #404, Naruto Chapter #408, "
            "Naruto Chapter #410, Naruto Chapter #411"
        ),
        "expected_arc": "Fated Battle Between Brothers",
        "notes": "Start of benchmark arc.",
    },
    148: {
        "classification": "arc_start",
        "mapping_shape": "none",
        "expects_chapter_mapping": False,
        "expects_arc": True,
        "expected_title": "Heir to Darkness",
        "expected_chapter_text": "",
        "expected_arc": "Six-Tails Unleashed",
        "notes": "Start of benchmark arc. No manga chapter mapping.",
    },
    158: {
        "classification": "arc_start",
        "mapping_shape": "multiple",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Power to Believe",
        "expected_chapter_text": (
            "Naruto Chapter #420, Naruto Chapter #421, Naruto Chapter #422"
        ),
        "expected_arc": "Pain's Assault",
        "notes": "Start of benchmark arc.",
    },
}

REQUIRED_FIELDS = {
    "classification",
    "mapping_shape",
    "expects_chapter_mapping",
    "expects_arc",
    "expected_title",
    "expected_chapter_text",
    "expected_arc",
    "notes",
}

ALLOWED_MAPPING_SHAPES = {
    "single",
    "multiple",
    "none",
    "unknown",
}


# ============================================================================
# Helper functions
# ============================================================================

def fixture_path(episode_number: int) -> Path:
    """Return the fixture path for one benchmark episode."""

    return FIXTURE_ROOT / f"episode_{episode_number:03d}.html"


def load_html(episode_number: int) -> str:
    """Load one fixture as UTF-8 text."""

    path = fixture_path(episode_number)

    assert path.is_file(), f"Missing fixture: {path}"

    html = path.read_text(encoding="utf-8")

    assert html.strip(), f"Fixture is empty: {path}"

    return html


def load_soup(episode_number: int) -> BeautifulSoup:
    """Parse one fixture with BeautifulSoup."""

    return BeautifulSoup(load_html(episode_number), "html.parser")


def normalize_text(value: str) -> str:
    """Normalize source whitespace and punctuation spacing."""

    normalized = re.sub(r"\s+", " ", value).strip()
    normalized = re.sub(r"\s+,", ",", normalized)
    normalized = re.sub(r",\s*", ", ", normalized)

    return normalized


def title_text(title_element: Tag) -> str:
    """Read the episode title without the Fandom edit-control text."""

    cleaned_title = copy(title_element)

    for control in cleaned_title.select(
        'a[href*="Special:FormEdit"], span[style*="float:right"]'
    ):
        control.decompose()

    value = normalize_text(cleaned_title.get_text(" ", strip=True))

    return value.strip('"“”')


def selected_value_text(
    soup: BeautifulSoup,
    value_selector: str,
    fallback_selector: str,
) -> str:
    """Read a Portable Infobox value, falling back to its full field."""

    element = soup.select_one(value_selector)

    if element is None:
        element = soup.select_one(fallback_selector)

    assert element is not None, (
        f"No element matched {value_selector!r} or {fallback_selector!r}"
    )

    return normalize_text(element.get_text(" ", strip=True))


def test_benchmark_episode_count():

    assert benchmark_episode_count() == 11


def test_benchmark_has_mapped_episodes():

    assert mapped_episode_count() > 0


def test_benchmark_has_unmapped_episodes():

    assert unmapped_episode_count() > 0


def test_every_episode_has_arc():

    assert arc_count() == benchmark_episode_count()


# ============================================================================
# Fixture integrity
# ============================================================================

@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_fixture_exists(episode_number: int) -> None:
    assert fixture_path(episode_number).is_file()


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_fixture_is_not_empty(episode_number: int) -> None:
    assert load_html(episode_number).strip()


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_fixture_parses_as_html(episode_number: int) -> None:
    soup = load_soup(episode_number)

    assert soup.find() is not None


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_fixture_has_document_root(episode_number: int) -> None:
    soup = load_soup(episode_number)

    assert soup.html is not None
    assert soup.body is not None


# ============================================================================
# Registry integrity
# ============================================================================

def test_registry_matches_benchmark() -> None:
    assert set(EXPECTED_EPISODES) == set(BENCHMARK_EPISODES)


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_registry_record_is_complete(episode_number: int) -> None:
    record = EXPECTED_EPISODES[episode_number]

    assert REQUIRED_FIELDS <= record.keys()
    assert record["mapping_shape"] in ALLOWED_MAPPING_SHAPES
    assert record["expected_title"].strip()
    assert record["notes"].strip()


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_mapping_expectations_are_consistent(episode_number: int) -> None:
    record = EXPECTED_EPISODES[episode_number]
    mapping_shape = record["mapping_shape"]

    if mapping_shape == "none":
        assert record["expects_chapter_mapping"] is False
        assert record["expected_chapter_text"] == ""
    elif mapping_shape in {"single", "multiple"}:
        assert record["expects_chapter_mapping"] is True
        assert record["expected_chapter_text"].strip()


def test_expected_titles_are_unique() -> None:
    titles = [
        EXPECTED_EPISODES[episode]["expected_title"]
        for episode in BENCHMARK_EPISODES
    ]

    assert len(titles) == len(set(titles))


def test_mapped_chapter_expectations_are_non_empty() -> None:
    mapped_records = [
        EXPECTED_EPISODES[episode]
        for episode in BENCHMARK_EPISODES
        if EXPECTED_EPISODES[episode]["expects_chapter_mapping"]
    ]

    assert mapped_records
    assert all(
        record["expected_chapter_text"].strip()
        for record in mapped_records
    )


@pytest.mark.parametrize(
    "episode_number",
    BENCHMARK_EPISODES,
)
def test_mapping_shape_consistency(
    episode_number,
):
    expected = EXPECTED_EPISODES[episode_number]

    shape = expected["mapping_shape"]

    if shape == "single":
        assert "," not in expected["expected_chapter_text"]

    elif shape == "multiple":
        assert "," in expected["expected_chapter_text"]

    elif shape == "none":
        assert expected["expected_chapter_text"] == ""


# ============================================================================
# Benchmark characterization schema
# ============================================================================

REQUIRED_CHARACTERIZATION_FIELDS = {
    "classification",
    "mapping_shape",
    "expects_chapter_mapping",
    "expects_arc",
    "expected_title",
    "expected_chapter_text",
    "expected_arc",
    "notes",
}

REQUIRED_SELECTOR_FIELDS = {
    "infobox",
    "title",
    "chapter",
    "chapter_value",
    "arc",
    "arc_value",
}

VALID_CLASSIFICATIONS = {
    "arc_start",
    "standalone",
    "canon",
    "filler",
    "anime_original",
    "mixed",
}


@pytest.mark.parametrize(
    "episode_number",
    BENCHMARK_EPISODES,
)
def test_classification_is_valid(
    episode_number,
):
    classification = (
        EXPECTED_EPISODES[episode_number]["classification"]
    )

    assert classification in VALID_CLASSIFICATIONS


@pytest.mark.parametrize(
    "episode_number",
    BENCHMARK_EPISODES,
)
def test_notes_are_documented(
    episode_number,
):
    notes = EXPECTED_EPISODES[episode_number]["notes"]

    assert notes.strip()

    assert 10 <= len(notes) <= 200


def test_selector_registry_is_complete():
    assert REQUIRED_SELECTOR_FIELDS <= DEFAULT_SELECTORS.keys()


def test_selector_values_are_strings():

    for selector in DEFAULT_SELECTORS.values():

        assert isinstance(selector, str)

        assert selector.strip()


@pytest.mark.parametrize(
    "episode_number",
    BENCHMARK_EPISODES,
)
def test_characterization_schema_complete(
    episode_number,
):
    record = EXPECTED_EPISODES[episode_number]

    assert REQUIRED_CHARACTERIZATION_FIELDS <= record.keys()


@pytest.mark.parametrize(
    "episode_number",
    BENCHMARK_EPISODES,
)
def test_expectation_types(
    episode_number,
):
    record = EXPECTED_EPISODES[episode_number]

    assert isinstance(record["classification"], str)

    assert isinstance(record["mapping_shape"], str)

    assert isinstance(
        record["expects_chapter_mapping"],
        bool,
    )

    assert isinstance(
        record["expects_arc"],
        bool,
    )

    assert isinstance(
        record["expected_title"],
        str,
    )

    assert isinstance(
        record["expected_chapter_text"],
        str,
    )

    assert isinstance(
        record["expected_arc"],
        str,
    )

    assert isinstance(
        record["notes"],
        str,
    )


def test_registry_episode_order():

    assert tuple(EXPECTED_EPISODES.keys()) == BENCHMARK_EPISODES


def test_registry_has_no_duplicate_keys():

    assert len(EXPECTED_EPISODES) == len(
        set(EXPECTED_EPISODES)
    )


# ============================================================================
# Benchmark metadata validation
# ============================================================================


def test_benchmark_name():
    assert BENCHMARK_NAME == "Naruto Shippuden"


def test_source_provider():
    assert SOURCE_PROVIDER == "Fandom"


def test_source_type():
    assert SOURCE_TYPE == "Episode"


def test_benchmark_version():
    assert BENCHMARK_VERSION.startswith("v")

def test_metadata_types():

    assert isinstance(BENCHMARK_NAME, str)

    assert isinstance(SOURCE_PROVIDER, str)

    assert isinstance(SOURCE_TYPE, str)

    assert isinstance(BENCHMARK_VERSION, str)


# ============================================================================
# Structural characterization
# ============================================================================

@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_has_infobox(episode_number: int) -> None:
    soup = load_soup(episode_number)

    assert soup.select_one(DEFAULT_SELECTORS["infobox"]) is not None


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_has_title(episode_number: int) -> None:
    soup = load_soup(episode_number)
    title = soup.select_one(DEFAULT_SELECTORS["title"])

    assert title is not None
    assert title_text(title)


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_chapter_structure_matches_characterization(
    episode_number: int,
) -> None:
    soup = load_soup(episode_number)
    expected = EXPECTED_EPISODES[episode_number]
    chapter = soup.select_one(DEFAULT_SELECTORS["chapter"])

    if expected["expects_chapter_mapping"]:
        assert chapter is not None
        assert chapter.get_text(" ", strip=True)


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_has_arc_section(episode_number: int) -> None:
    soup = load_soup(episode_number)
    expected = EXPECTED_EPISODES[episode_number]
    arc = soup.select_one(DEFAULT_SELECTORS["arc"])

    if expected["expects_arc"]:
        assert arc is not None
        assert arc.get_text(" ", strip=True)


# ============================================================================
# Metadata-value characterization
# ============================================================================

@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_title_matches_characterization(
    episode_number: int,
) -> None:
    soup = load_soup(episode_number)
    expected = EXPECTED_EPISODES[episode_number]
    title = soup.select_one(DEFAULT_SELECTORS["title"])

    assert title is not None

    actual = title_text(title)

    assert actual == expected["expected_title"]


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_chapter_text_matches_characterization(
    episode_number: int,
) -> None:
    expected = EXPECTED_EPISODES[episode_number]

    if not expected["expects_chapter_mapping"]:
        pytest.skip("Episode intentionally has no chapter mapping.")

    soup = load_soup(episode_number)

    actual = selected_value_text(
        soup,
        DEFAULT_SELECTORS["chapter_value"],
        DEFAULT_SELECTORS["chapter"],
    )

    assert actual == normalize_text(expected["expected_chapter_text"])


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_arc_matches_characterization(
    episode_number: int,
) -> None:
    expected = EXPECTED_EPISODES[episode_number]

    if not expected["expects_arc"]:
        pytest.skip("Episode intentionally has no arc.")

    soup = load_soup(episode_number)

    actual = selected_value_text(
        soup,
        DEFAULT_SELECTORS["arc_value"],
        DEFAULT_SELECTORS["arc"],
    )

    assert actual == normalize_text(expected["expected_arc"])


# ============================================================================
# Benchmark statistics
# ============================================================================


def benchmark_episode_count():

    return len(BENCHMARK_EPISODES)


def mapped_episode_count():

    return sum(
        episode["expects_chapter_mapping"]
        for episode in EXPECTED_EPISODES.values()
    )


def unmapped_episode_count():

    return sum(
        not episode["expects_chapter_mapping"]
        for episode in EXPECTED_EPISODES.values()
    )


def arc_count():

    return sum(
        episode["expects_arc"]
        for episode in EXPECTED_EPISODES.values()
    )


# ============================================================================
# Regression protection
# ============================================================================

def test_fixture_inventory_matches_benchmark() -> None:
    expected = {
        f"episode_{episode:03d}.html"
        for episode in BENCHMARK_EPISODES
    }

    actual = {
        path.name
        for path in FIXTURE_ROOT.glob("episode_*.html")
    }

    assert expected == actual


def test_episode_numbers_are_unique_and_ordered() -> None:
    assert len(BENCHMARK_EPISODES) == len(set(BENCHMARK_EPISODES))
    assert tuple(sorted(BENCHMARK_EPISODES)) == BENCHMARK_EPISODES


def test_benchmark_size() -> None:
    assert len(BENCHMARK_EPISODES) == 11