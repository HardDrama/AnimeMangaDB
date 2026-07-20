"""
Boruto source-page characterization tests.

These tests preserve the observed structure and metadata values of the
Boruto benchmark episode pages before production implementation.

The tests intentionally inspect stored HTML fixtures directly. They do not
call production providers, extractors, repositories, APIs, database code, or
network resources.

The expected values in this module were derived from the stored fixture
observation report produced during v0.64.4.
"""

from copy import copy
from pathlib import Path
import re

import pytest
from bs4 import BeautifulSoup, Tag


# ============================================================================
# Benchmark metadata
# ============================================================================

BENCHMARK_NAME = "Boruto"

SOURCE_PROVIDER = "Fandom"

SOURCE_TYPE = "Episode"

BENCHMARK_VERSION = "v0.64.5"


# ============================================================================
# Fixture locations and benchmark scope
# ============================================================================

FIXTURE_ROOT = (
    Path(__file__).parent
    / "fixtures"
    / "boruto"
    / "episodes"
)

BENCHMARK_EPISODES = (
    1,
    19,
    39,
    53,
    65,
    148,
    181,
    189,
    192,
    220,
    287,
    293,
)


# ============================================================================
# Observed selectors
# ============================================================================

DEFAULT_SELECTORS = {
    "infobox": "aside.portable-infobox",
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
        "classification": "series_opening",
        "mapping_shape": "single",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Boruto Uzumaki!!",
        "expected_chapter_text": "Boruto Chapter #1",
        "expected_arc": "Academy Entrance Arc",
        "notes": (
            "Series-opening benchmark with one observed Boruto chapter mapping."
        ),
    },
    19: {
        "classification": "early_adaptation",
        "mapping_shape": "multiple",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Sarada Uchiha",
        "expected_chapter_text": (
            "Naruto Chapter #700+1, Naruto Chapter #700+2"
        ),
        "expected_arc": "Sarada Uchiha Arc",
        "notes": (
            "Early adaptation using Naruto side-story chapter numbering."
        ),
    },
    39: {
        "classification": "standalone_adaptation",
        "mapping_shape": "single",
        "expects_chapter_mapping": True,
        "expects_arc": False,
        "expected_title": "The Path Lit by the Full Moon",
        "expected_chapter_text": "Boruto Chapter #0",
        "expected_arc": "",
        "notes": (
            "Standalone Chapter 0 adaptation whose fixture has no arc field."
        ),
    },
    53: {
        "classification": "arc_start",
        "mapping_shape": "single",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Himawari's Birthday",
        "expected_chapter_text": "Boruto Chapter #1",
        "expected_arc": "Versus Momoshiki Arc",
        "notes": (
            "Beginning of the selected Versus Momoshiki benchmark segment."
        ),
    },
    65: {
        "classification": "arc_climax",
        "mapping_shape": "multiple",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Father and Child",
        "expected_chapter_text": (
            "Boruto Chapter #8, Boruto Chapter #9, Boruto Chapter #10"
        ),
        "expected_arc": "Versus Momoshiki Arc",
        "notes": (
            "High-density multi-chapter adaptation at a major arc climax."
        ),
    },
    148: {
        "classification": "arc_start",
        "mapping_shape": "single",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "A New Mission!!",
        "expected_chapter_text": "Boruto Chapter #11",
        "expected_arc": "Mujina Bandits Arc",
        "notes": (
            "Start of the selected Mujina Bandits manga adaptation segment."
        ),
    },
    181: {
        "classification": "arc_start",
        "mapping_shape": "single",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "The Vessel",
        "expected_chapter_text": "Boruto Chapter #16",
        "expected_arc": "Ao Arc",
        "notes": (
            "Start of the selected Ao and Vessel adaptation sequence."
        ),
    },
    189: {
        "classification": "character_boundary",
        "mapping_shape": "single",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Resonance",
        "expected_chapter_text": "Boruto Chapter #25",
        "expected_arc": "Kawaki Arc",
        "notes": (
            "Kawaki-era boundary case with one observed chapter mapping."
        ),
    },
    192: {
        "classification": "mixed_adaptation",
        "mapping_shape": "multiple",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "The Past",
        "expected_chapter_text": (
            "Boruto Chapter #24, Boruto Chapter #26"
        ),
        "expected_arc": "Kawaki Arc",
        "notes": (
            "Mixed benchmark with two non-consecutive chapter references."
        ),
    },
    220: {
        "classification": "arc_conclusion",
        "mapping_shape": "multiple",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Remaining Time",
        "expected_chapter_text": (
            "Boruto Chapter #56, Boruto Chapter #57, Boruto Chapter #58"
        ),
        "expected_arc": "Kawaki Arc",
        "notes": (
            "Late Kawaki Arc conclusion with three consecutive mappings."
        ),
    },
    287: {
        "classification": "arc_start",
        "mapping_shape": "multiple",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Claw Marks",
        "expected_chapter_text": (
            "Boruto Chapter #55, Boruto Chapter #56, "
            "Boruto Chapter #57, Boruto Chapter #60"
        ),
        "expected_arc": "Code's Assault Arc",
        "notes": (
            "Start of the final selected arc with non-consecutive mappings."
        ),
    },
    293: {
        "classification": "series_finale",
        "mapping_shape": "multiple",
        "expects_chapter_mapping": True,
        "expects_arc": True,
        "expected_title": "Farewell",
        "expected_chapter_text": (
            "Boruto Chapter #67, Boruto Chapter #68, Boruto Chapter #70"
        ),
        "expected_arc": "Code's Assault Arc",
        "notes": (
            "Series-finale benchmark with three observed chapter references."
        ),
    },
}


# ============================================================================
# Characterization schema
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

ALLOWED_MAPPING_SHAPES = {
    "single",
    "multiple",
    "none",
    "unknown",
}

VALID_CLASSIFICATIONS = {
    "series_opening",
    "early_adaptation",
    "standalone_adaptation",
    "arc_start",
    "arc_climax",
    "character_boundary",
    "mixed_adaptation",
    "arc_conclusion",
    "series_finale",
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
    """Normalize source whitespace and comma spacing."""

    normalized = re.sub(r"\s+", " ", value).strip()
    normalized = re.sub(r"\s+,", ",", normalized)
    normalized = re.sub(r",\s*", ", ", normalized)

    return normalized


def title_text(title_element: Tag) -> str:
    """Read the episode title without Fandom edit-control text."""

    cleaned_title = copy(title_element)

    for control in cleaned_title.select(
        'a[href*="Special:FormEdit"], '
        'a[title*="edit" i], '
        'span[style*="float:right"]'
    ):
        control.decompose()

    value = normalize_text(cleaned_title.get_text(" ", strip=True))

    return value.strip("\"“”")


def selected_value_text(
    soup: BeautifulSoup,
    value_selector: str,
    fallback_selector: str,
) -> str:
    """Read a Portable Infobox value, falling back to the full field."""

    element = soup.select_one(value_selector)

    if element is None:
        element = soup.select_one(fallback_selector)

    assert element is not None, (
        f"No element matched {value_selector!r} or {fallback_selector!r}"
    )

    return normalize_text(element.get_text(" ", strip=True))


def benchmark_episode_count() -> int:
    return len(BENCHMARK_EPISODES)


def mapped_episode_count() -> int:
    return sum(
        record["expects_chapter_mapping"]
        for record in EXPECTED_EPISODES.values()
    )


def unmapped_episode_count() -> int:
    return sum(
        not record["expects_chapter_mapping"]
        for record in EXPECTED_EPISODES.values()
    )


def arc_episode_count() -> int:
    return sum(
        record["expects_arc"]
        for record in EXPECTED_EPISODES.values()
    )


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
# Benchmark metadata validation
# ============================================================================

def test_benchmark_name() -> None:
    assert BENCHMARK_NAME == "Boruto"


def test_source_provider() -> None:
    assert SOURCE_PROVIDER == "Fandom"


def test_source_type() -> None:
    assert SOURCE_TYPE == "Episode"


def test_benchmark_version() -> None:
    assert BENCHMARK_VERSION == "v0.64.5"


def test_metadata_types() -> None:
    assert isinstance(BENCHMARK_NAME, str)
    assert isinstance(SOURCE_PROVIDER, str)
    assert isinstance(SOURCE_TYPE, str)
    assert isinstance(BENCHMARK_VERSION, str)


# ============================================================================
# Selector validation
# ============================================================================

def test_selector_registry_is_complete() -> None:
    assert REQUIRED_SELECTOR_FIELDS <= DEFAULT_SELECTORS.keys()


def test_selector_values_are_strings() -> None:
    for selector in DEFAULT_SELECTORS.values():
        assert isinstance(selector, str)
        assert selector.strip()


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_observed_infobox_selector_matches(
    episode_number: int,
) -> None:
    soup = load_soup(episode_number)

    assert soup.select_one(DEFAULT_SELECTORS["infobox"]) is not None


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_observed_title_selector_matches(
    episode_number: int,
) -> None:
    soup = load_soup(episode_number)

    assert soup.select_one(DEFAULT_SELECTORS["title"]) is not None


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_observed_chapter_selector_matches(
    episode_number: int,
) -> None:
    soup = load_soup(episode_number)

    assert soup.select_one(DEFAULT_SELECTORS["chapter"]) is not None
    assert soup.select_one(DEFAULT_SELECTORS["chapter_value"]) is not None


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_observed_arc_selector_matches_characterization(
    episode_number: int,
) -> None:
    soup = load_soup(episode_number)
    expected = EXPECTED_EPISODES[episode_number]

    arc = soup.select_one(DEFAULT_SELECTORS["arc"])
    arc_value = soup.select_one(DEFAULT_SELECTORS["arc_value"])

    if expected["expects_arc"]:
        assert arc is not None
        assert arc_value is not None
    else:
        assert arc is None
        assert arc_value is None


# ============================================================================
# Registry validation
# ============================================================================

def test_registry_matches_benchmark() -> None:
    assert set(EXPECTED_EPISODES) == set(BENCHMARK_EPISODES)


def test_registry_episode_order() -> None:
    assert tuple(EXPECTED_EPISODES.keys()) == BENCHMARK_EPISODES


def test_registry_has_no_duplicate_keys() -> None:
    assert len(EXPECTED_EPISODES) == len(set(EXPECTED_EPISODES))


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_characterization_schema_complete(
    episode_number: int,
) -> None:
    record = EXPECTED_EPISODES[episode_number]

    assert REQUIRED_CHARACTERIZATION_FIELDS <= record.keys()


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_expectation_types(episode_number: int) -> None:
    record = EXPECTED_EPISODES[episode_number]

    assert isinstance(record["classification"], str)
    assert isinstance(record["mapping_shape"], str)
    assert isinstance(record["expects_chapter_mapping"], bool)
    assert isinstance(record["expects_arc"], bool)
    assert isinstance(record["expected_title"], str)
    assert isinstance(record["expected_chapter_text"], str)
    assert isinstance(record["expected_arc"], str)
    assert isinstance(record["notes"], str)


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_classification_is_valid(episode_number: int) -> None:
    classification = EXPECTED_EPISODES[episode_number]["classification"]

    assert classification in VALID_CLASSIFICATIONS


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_mapping_shape_is_valid(episode_number: int) -> None:
    mapping_shape = EXPECTED_EPISODES[episode_number]["mapping_shape"]

    assert mapping_shape in ALLOWED_MAPPING_SHAPES


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_mapping_shape_consistency(episode_number: int) -> None:
    record = EXPECTED_EPISODES[episode_number]
    mapping_shape = record["mapping_shape"]
    chapter_text = record["expected_chapter_text"]

    if mapping_shape == "single":
        assert "," not in chapter_text
        assert chapter_text.strip()
        assert record["expects_chapter_mapping"] is True

    elif mapping_shape == "multiple":
        assert "," in chapter_text
        assert chapter_text.strip()
        assert record["expects_chapter_mapping"] is True

    elif mapping_shape == "none":
        assert chapter_text == ""
        assert record["expects_chapter_mapping"] is False


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_arc_expectation_consistency(episode_number: int) -> None:
    record = EXPECTED_EPISODES[episode_number]

    if record["expects_arc"]:
        assert record["expected_arc"].strip()
    else:
        assert record["expected_arc"] == ""


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_notes_are_documented(episode_number: int) -> None:
    notes = EXPECTED_EPISODES[episode_number]["notes"]

    assert notes.strip()
    assert 10 <= len(notes) <= 200


def test_expected_titles_are_unique() -> None:
    titles = [
        EXPECTED_EPISODES[episode]["expected_title"]
        for episode in BENCHMARK_EPISODES
    ]

    assert len(titles) == len(set(titles))


# ============================================================================
# Structural characterization
# ============================================================================

@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_has_infobox(episode_number: int) -> None:
    soup = load_soup(episode_number)

    infobox = soup.select_one(DEFAULT_SELECTORS["infobox"])

    assert infobox is not None
    assert "type-episode" in infobox.get("class", [])


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_has_title(episode_number: int) -> None:
    soup = load_soup(episode_number)
    title = soup.select_one(DEFAULT_SELECTORS["title"])

    assert title is not None
    assert title_text(title)


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_has_chapter_section(episode_number: int) -> None:
    soup = load_soup(episode_number)
    chapter = soup.select_one(DEFAULT_SELECTORS["chapter"])
    chapter_value = soup.select_one(DEFAULT_SELECTORS["chapter_value"])

    assert chapter is not None
    assert chapter_value is not None
    assert chapter_value.get_text(" ", strip=True)


@pytest.mark.parametrize("episode_number", BENCHMARK_EPISODES)
def test_episode_arc_structure_matches_characterization(
    episode_number: int,
) -> None:
    soup = load_soup(episode_number)
    expected = EXPECTED_EPISODES[episode_number]

    arc = soup.select_one(DEFAULT_SELECTORS["arc"])
    arc_value = soup.select_one(DEFAULT_SELECTORS["arc_value"])

    if expected["expects_arc"]:
        assert arc is not None
        assert arc_value is not None
        assert arc_value.get_text(" ", strip=True)
    else:
        assert arc is None
        assert arc_value is None


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

def test_benchmark_episode_count() -> None:
    assert benchmark_episode_count() == 12


def test_all_selected_episodes_have_chapter_mappings() -> None:
    assert mapped_episode_count() == benchmark_episode_count()
    assert unmapped_episode_count() == 0


def test_one_selected_episode_has_no_arc() -> None:
    assert arc_episode_count() == 11


def test_benchmark_contains_single_and_multiple_mappings() -> None:
    mapping_shapes = {
        record["mapping_shape"]
        for record in EXPECTED_EPISODES.values()
    }

    assert "single" in mapping_shapes
    assert "multiple" in mapping_shapes


def test_benchmark_contains_naruto_and_boruto_chapter_namespaces() -> None:
    chapter_values = [
        record["expected_chapter_text"]
        for record in EXPECTED_EPISODES.values()
    ]

    assert any(value.startswith("Naruto Chapter") for value in chapter_values)
    assert any(value.startswith("Boruto Chapter") for value in chapter_values)


def test_benchmark_contains_non_consecutive_mapping_cases() -> None:
    assert (
        EXPECTED_EPISODES[192]["expected_chapter_text"]
        == "Boruto Chapter #24, Boruto Chapter #26"
    )

    assert (
        EXPECTED_EPISODES[287]["expected_chapter_text"]
        == (
            "Boruto Chapter #55, Boruto Chapter #56, "
            "Boruto Chapter #57, Boruto Chapter #60"
        )
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
    assert len(BENCHMARK_EPISODES) == 12
