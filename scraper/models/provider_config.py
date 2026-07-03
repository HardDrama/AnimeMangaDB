from pydantic import BaseModel


class SelectorConfig(BaseModel):
    title: str
    chapter: str
    arc: str


class ScraperConfig(BaseModel):
    max_episodes: int
    start_episode: int | None = None
    end_episode: int | None = None
    full_crawl: bool = False
    config_path: str | None = None


class ProviderConfig(BaseModel):
    series: str
    base_url: str
    episode_path: str
    selectors: SelectorConfig
    scraper: ScraperConfig