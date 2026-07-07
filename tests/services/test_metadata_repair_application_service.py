import pytest

from scraper.models.metadata_repair import MetadataRepair
from scraper.models.metadata_repair_plan import MetadataRepairPlan
from scraper.services.metadata_repair_application_service import (
    MetadataRepairApplicationService,
)


class DummyEpisode:
    episode_title = "Episode 1"
    arc = None
    source_url = "https://example.com/episode/1"


def test_applies_title_and_arc_repairs():
    episode = DummyEpisode()

    plan = MetadataRepairPlan(
        repairs=[
            MetadataRepair(
                field="title",
                current_value="Episode 1",
                new_value="I'm Luffy! The Man Who Will Become the Pirate King!",
            ),
            MetadataRepair(
                field="arc",
                current_value=None,
                new_value="Romance Dawn Arc",
            ),
        ]
    )

    service = MetadataRepairApplicationService()

    result = service.apply(
        episode,
        plan,
    )

    assert result.applied == 2
    assert result.skipped == 0
    assert (
        episode.episode_title
        == "I'm Luffy! The Man Who Will Become the Pirate King!"
    )
    assert episode.arc == "Romance Dawn Arc"
    assert result.committed is False


def test_skips_unsupported_repairs():
    episode = DummyEpisode()

    plan = MetadataRepairPlan(
        repairs=[
            MetadataRepair(
                field="source_url",
                current_value="https://example.com/episode/1",
                new_value="https://example.com/episode/1",
            ),
        ]
    )

    service = MetadataRepairApplicationService()

    result = service.apply(
        episode,
        plan,
    )

    assert result.applied == 0
    assert result.skipped == 1

def test_commit_requires_session():
    episode = DummyEpisode()

    plan = MetadataRepairPlan()

    service = MetadataRepairApplicationService()

    with pytest.raises(ValueError):
        service.apply(
            episode,
            plan,
            commit=True,
        )