from scraper.database.base import Base
from scraper.database.models import (
    Anime,
    ChapterMetadata,
    Episode,
    EpisodeChapter,
)
from scraper.database.migrations import (
    run_pending_migrations,
)
from scraper.database.session import engine


# Keep model imports explicit so SQLAlchemy registers all tables
# before create_all() executes.
del Anime
del ChapterMetadata
del Episode
del EpisodeChapter


Base.metadata.create_all(
    bind=engine
)

migration_result = run_pending_migrations(
    engine
)

print("Database initialized successfully!")
print(
    "Database migrations applied: "
    f"{migration_result.applied_count}"
)
print(
    "Database migrations skipped: "
    f"{migration_result.skipped_count}"
)