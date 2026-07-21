from sqlalchemy.orm import Session

from scraper.repositories.episode_repository_shared_manga import (
    EpisodeRepository,
)
from scraper.repositories.manga_repository_shared_manga import (
    MangaRepository,
)
from scraper.services.shared_manga_api_service import (
    SharedMangaApiService,
)


def build_staged_api_service(
    session: Session,
) -> SharedMangaApiService:
    """
    Compose the dormant shared-manga API service.

    This provider is intentionally not connected to production routes
    or runtime factories during v0.65.3.
    """

    return SharedMangaApiService(
        episode_repository=EpisodeRepository(session),
        manga_repository=MangaRepository(session),
    )
