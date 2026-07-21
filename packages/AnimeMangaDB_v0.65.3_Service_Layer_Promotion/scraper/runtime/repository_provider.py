from scraper.repositories.episode_repository import EpisodeRepository
from scraper.repositories.episode_repository_shared_manga import (
    EpisodeRepository as StagedEpisodeRepository,
)
from scraper.repositories.manga_repository import MangaRepository
from scraper.repositories.manga_repository_shared_manga import (
    MangaRepository as StagedMangaRepository,
)


class RuntimeRepositoryProvider:
    """
    Central registry for production and staged repository
    implementations.
    """

    production_episode_repository = EpisodeRepository
    production_chapter_repository = MangaRepository

    staged_episode_repository = StagedEpisodeRepository
    staged_chapter_repository = StagedMangaRepository
