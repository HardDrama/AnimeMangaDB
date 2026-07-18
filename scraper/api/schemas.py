from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class EpisodeResponse(BaseModel):
    id: int
    anime_id: int | None = None
    anime_title: str
    episode_number: int

    # Canonical Scope v2 field.
    episode_title: str | None = None

    # Scope v1 frontend compatibility field.
    title: str | None = None

    arc: str | None = None
    source_url: str | None = None


class EpisodeListResponse(BaseModel):
    episodes: list[EpisodeResponse]

class ChapterMetadataResponse(BaseModel):
    chapter_number: int
    chapter_title: str
    manga_arc: str | None = None
    source_url: str
    last_updated: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class ChapterMetadataSearchResponse(
    ChapterMetadataResponse
):
    anime_id: int
    anime_title: str

class ChapterMappingResponse(BaseModel):
    chapter_number: int

class ArcSummaryResponse(BaseModel):
    name: str
    episode_arc: str | None = None
    manga_arc: str | None = None
    episode_count: int = 0
    chapter_count: int = 0

class SeriesResponse(BaseModel):
    id: int
    title: str
    provider: str
    base_url: str | None = None
    episode_count: int | None = None
    chapter_count: int | None = None

class SeriesListResponse(BaseModel):
    series: list[SeriesResponse]

class ChapterSearchResult(BaseModel):
    chapter_number: int
    episodes: list[EpisodeResponse]

class SearchResponse(BaseModel):
    anime: list[SeriesResponse]
    episodes: list[EpisodeResponse]
    chapters: list[ChapterSearchResult]
    chapter_metadata: list[
        ChapterMetadataSearchResponse
    ] = Field(
        default_factory=list,
    )