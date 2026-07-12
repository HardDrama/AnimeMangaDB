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


class ChapterMetadataConfig(BaseModel):
    index_path: str
    url_strategy: str
    chapter_path: str | None = None
    index_section_id: str | None = None

class ChapterSelectorConfig(BaseModel):
    title: str | None = None
    manga_arc: str | None = None
    title_strategy: str
    arc_strategy: str


class ProviderConfig(BaseModel):
    series: str
    base_url: str
    episode_path: str
    selectors: SelectorConfig
    chapter_metadata: ChapterMetadataConfig | None = None
    chapter_selectors: ChapterSelectorConfig | None = None
    scraper: ScraperConfig