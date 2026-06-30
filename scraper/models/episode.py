from datetime import datetime
from typing import Optional
from typing import List

from pydantic import BaseModel, Field, HttpUrl

class EpisodeData(BaseModel):
    anime_title: str

    episode_number: int
    episode_title: str

    chapter_numbers: List[int] = []

    arc: Optional[str] = None

    source_url: HttpUrl

    last_updated: datetime = Field(default_factory=datetime.now)