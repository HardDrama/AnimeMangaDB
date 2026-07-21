from scraper.repositories import episode_repository
from scraper.repositories import chapter_metadata_repository

from scraper.repositories import (
    episode_repository_shared_manga,
    manga_repository_shared_manga,
)


class RuntimeRepositoryProvider:
    """
    Repository compatibility layer.

    Production repositories remain active until the shared
    runtime is promoted.
    """

    production_episode = episode_repository
    production_chapter = chapter_metadata_repository

    staged_episode = episode_repository_shared_manga
    staged_manga = manga_repository_shared_manga