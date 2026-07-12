from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChapterMetadata:
    chapter_number: int
    chapter_title: str | None = None
    manga_arc: str | None = None
    source_url: str | None = None
    last_updated: datetime | None = None