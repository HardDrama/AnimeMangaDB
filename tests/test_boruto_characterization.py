"""
Boruto source-page characterization tests.

These tests preserve the observed structure of Boruto episode pages prior
to production implementation.

The tests intentionally inspect stored HTML fixtures directly and do not
call providers, extractors, repositories, APIs, or database code.
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


# ============================================================================
# Benchmark metadata
# ============================================================================

BENCHMARK_NAME = "Boruto"

SOURCE_PROVIDER = "Fandom"

SOURCE_TYPE = "Episode"

BENCHMARK_VERSION = "v0.64.3"


# ============================================================================
# Fixture locations
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
# Shared selectors
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
# Placeholder characterization registry
# ============================================================================

EXPECTED_EPISODES = {
    episode: {
        "classification": "unknown",
        "mapping_shape": "unknown",
        "expects_chapter_mapping": False,
        "expects_arc": False,
        "expected_title": "",
        "expected_chapter_text": "",
        "expected_arc": "",
        "notes": "",
    }
    for episode in BENCHMARK_EPISODES
}


# ============================================================================
# Helper functions
# ============================================================================

def fixture_path(episode_number: int) -> Path:
    return FIXTURE_ROOT / f"episode_{episode_number:03d}.html"


def load_html(episode_number: int) -> str:
    path = fixture_path(episode_number)

    assert path.exists()

    return path.read_text(encoding="utf-8")


def load_soup(episode_number: int) -> BeautifulSoup:
    return BeautifulSoup(load_html(episode_number), "html.parser")


# ============================================================================
# Foundation tests
# ============================================================================

def test_benchmark_name():
    assert BENCHMARK_NAME == "Boruto"


def test_fixture_count():
    assert len(BENCHMARK_EPISODES) == 12


@pytest.mark.parametrize(
    "episode_number",
    BENCHMARK_EPISODES,
)
def test_fixture_exists(episode_number):
    assert fixture_path(episode_number).exists()


@pytest.mark.parametrize(
    "episode_number",
    BENCHMARK_EPISODES,
)
def test_fixture_is_not_empty(
    episode_number,
):
    html = load_html(episode_number)

    assert html.strip()


@pytest.mark.parametrize(
    "episode_number",
    BENCHMARK_EPISODES,
)
def test_fixture_parses(
    episode_number,
):
    soup = load_soup(episode_number)

    assert soup.find() is not None


@pytest.mark.parametrize(
    "episode_number",
    BENCHMARK_EPISODES,
)
def test_fixture_has_document_root(
    episode_number,
):
    soup = load_soup(episode_number)

    assert soup.html is not None

    assert soup.body is not None


def test_registry_matches_benchmark():
    assert set(EXPECTED_EPISODES) == set(
        BENCHMARK_EPISODES
    )


def test_selector_registry_complete():

    assert {
        "infobox",
        "title",
        "chapter",
        "chapter_value",
        "arc",
        "arc_value",
    } <= DEFAULT_SELECTORS.keys()