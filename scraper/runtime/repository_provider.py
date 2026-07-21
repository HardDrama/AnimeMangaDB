from scraper.repositories.episode_repository import (
    EpisodeRepository as LegacyEpisodeRepository,
)
from scraper.repositories.episode_repository_shared_manga import (
    EpisodeRepository as SharedMangaEpisodeRepository,
)
from scraper.repositories.manga_repository_shared_manga import (
    MangaRepository as SharedMangaRepository,
)


class RuntimeRepositoryProvider:
    """
    Central registry for repository implementations.

    The legacy runtime remains the production default until the ORM and
    database migration are activated together. The staged runtime remains
    available for explicit validation and future activation.
    """

    production_episode_repository = LegacyEpisodeRepository
    production_chapter_repository = LegacyEpisodeRepository

    staged_episode_repository = SharedMangaEpisodeRepository
    staged_chapter_repository = SharedMangaRepository
