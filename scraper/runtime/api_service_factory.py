from enum import Enum

from sqlalchemy.orm import Session

from scraper.runtime.repository_factory import (
    RuntimeRepositoryMode,
    create_repository_set,
)
from scraper.services.shared_manga_api_service import (
    SharedMangaApiService,
)


class RuntimeApiMode(str, Enum):
    """
    API runtime composition modes.
    """

    PRODUCTION = "production"
    SHARED_MANGA = "shared_manga"


def create_api_service(
    session: Session,
    mode: RuntimeApiMode = RuntimeApiMode.PRODUCTION,
) -> SharedMangaApiService:
    """
    Compose an API service from the selected runtime.

    During the mitigation phase this factory is used only for
    validation. No production routes are switched yet.
    """

    repository_mode = (
        RuntimeRepositoryMode.PRODUCTION
        if mode is RuntimeApiMode.PRODUCTION
        else RuntimeRepositoryMode.SHARED_MANGA
    )

    repositories = create_repository_set(
        session,
        repository_mode,
    )

    return SharedMangaApiService(
        episode_repository=repositories.episode,
        manga_repository=repositories.chapter,
    )