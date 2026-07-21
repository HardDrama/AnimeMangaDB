from unittest.mock import Mock

from scraper.api.service_provider import (
    build_staged_api_service,
)
from scraper.repositories.episode_repository_shared_manga import (
    EpisodeRepository,
)
from scraper.repositories.manga_repository_shared_manga import (
    MangaRepository,
)
from scraper.services.shared_manga_api_service import (
    SharedMangaApiService,
)


def test_build_staged_api_service_composes_shared_repositories():
    session = Mock()

    service = build_staged_api_service(session)

    assert isinstance(service, SharedMangaApiService)
    assert isinstance(
        service.episode_repository,
        EpisodeRepository,
    )
    assert isinstance(
        service.manga_repository,
        MangaRepository,
    )
    assert service.episode_repository.session is session
    assert service.manga_repository.session is session
