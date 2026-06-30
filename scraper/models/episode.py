from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

class EpisodeData(BaseModel):
    anime_title: str

    episode_number: int
    episode_title: str

    adapted_chapters: list[int] = Field(default_factory=list)

    manga_start: Optional[int] = None
    manga_end: Optional[int] = None

    arc: Optional[str] = None

    source_url: HttpUrl

    last_updated: datetime = Field(default_factory=datetime.now)