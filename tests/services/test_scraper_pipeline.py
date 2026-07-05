from scraper.services.scraper_pipeline import ScraperPipeline


class FakeProvider:
    def build_episode_url(self, episode_number: int) -> str:
        return f"https://example.com/episode/{episode_number}"


def test_pipeline_can_be_created():
    pipeline = ScraperPipeline(
        config=None,
        provider=FakeProvider(),
        client=None,
        extractor=None,
        repo=None,
    )

    assert pipeline.provider.build_episode_url(1) == (
        "https://example.com/episode/1"
    )