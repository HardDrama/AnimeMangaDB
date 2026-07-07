from scraper.models.episode_metadata import EpisodeMetadata
from scraper.services.metadata_repair_service import (
    MetadataRepairService,
)


class DummyEpisode:
    episode_title = "Episode 1"
    arc = None
    source_url = "https://example.com/episode/1"


def test_build_repair_plan_from_metadata_differences():
    service = MetadataRepairService()

    metadata = EpisodeMetadata(
        title="I'm Luffy! The Man Who Will Become the Pirate King!",
        arc="Romance Dawn Arc",
        source_url="https://example.com/episode/1",
    )

    plan = service.build_repair_plan(
        DummyEpisode(),
        metadata,
    )

    assert plan.has_repairs is True
    assert len(plan.repairs) == 2

    fields = [
        repair.field
        for repair in plan.repairs
    ]

    assert "title" in fields
    assert "arc" in fields


def test_build_repair_plan_with_no_differences():
    service = MetadataRepairService()

    metadata = EpisodeMetadata(
        title="Episode 1",
        arc=None,
        source_url="https://example.com/episode/1",
    )

    plan = service.build_repair_plan(
        DummyEpisode(),
        metadata,
    )

    assert plan.has_repairs is False
    assert plan.repairs == []