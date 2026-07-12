from scraper.database.base import Base
from scraper.database.models import (
    Anime,
    ChapterMetadata,
    Episode,
    EpisodeChapter,
)
from scraper.database.session import engine

Base.metadata.create_all(bind=engine)

print("Database initialized successfully!")