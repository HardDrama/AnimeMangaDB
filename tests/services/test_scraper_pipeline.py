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

class FakeClient:
    def fetch(self, url: str) -> str:
        return "<html></html>"


class FakeEpisodeData:
    episode_number = 1
    episode_title = "Episode 1"
    manga_start = 1
    manga_end = 1
    arc = None
    source_url = "https://example.com/episode/1"
    last_updated = None


class FakeExtractor:
    def parse(self, html: str, episode_number: int, source_url: str):
        return FakeEpisodeData()


class FakeRepo:
    def get_or_create_anime(self, title, provider, base_url):
        return object()

    def create_episode(self, anime, data):
        return type(
            "SavedEpisode",
            (),
            {
                "id": 1,
                "episode_title": data.episode_title,
            },
        )()

    def chapter_mappings_need_update(self, episode, chapter_numbers):
        return True

    def replace_episode_chapters(self, episode, chapter_numbers):
        self.chapter_numbers = chapter_numbers


class FakeConfig:
    series = "Test Series"
    base_url = "https://example.com"


def test_pipeline_scrapes_episode_with_fake_dependencies():
    repo = FakeRepo()

    pipeline = ScraperPipeline(
        config=FakeConfig(),
        provider=FakeProvider(),
        client=FakeClient(),
        extractor=FakeExtractor(),
        repo=repo,
    )

    result = pipeline.scrape_episode(1)

    assert result["episode_number"] == 1
    assert result["has_chapters"] is True
    assert repo.chapter_numbers == [1]