import pytest
from sqlalchemy.orm import Session

from scraper.repositories.episode_repository import (
    EpisodeRepository as LegacyEpisodeRepository,
)
from scraper.repositories.episode_repository_shared_manga import (
    EpisodeRepository as SharedMangaEpisodeRepository,
)
from scraper.repositories.manga_repository_shared_manga import (
    MangaRepository,
)
from scraper.runtime.repository_factory import (
    RuntimeRepositoryMode,
    create_repository_set,
)
from scraper.runtime.repository_provider import (
    RuntimeRepositoryProvider,
)


def test_provider_exposes_legacy_repository_classes():
    assert (
        RuntimeRepositoryProvider
        .production_episode_repository
        is LegacyEpisodeRepository
    )
    assert (
        RuntimeRepositoryProvider
        .production_chapter_repository
        is LegacyEpisodeRepository
    )


def test_provider_exposes_shared_manga_repository_classes():
    assert (
        RuntimeRepositoryProvider
        .staged_episode_repository
        is SharedMangaEpisodeRepository
    )
    assert (
        RuntimeRepositoryProvider
        .staged_chapter_repository
        is MangaRepository
    )


def test_factory_defaults_to_production_runtime():
    session = Session()

    try:
        repositories = create_repository_set(
            session
        )

        assert (
            repositories.mode
            is RuntimeRepositoryMode.PRODUCTION
        )
        assert isinstance(
            repositories.episode,
            LegacyEpisodeRepository,
        )
        assert (
            repositories.episode
            is repositories.chapter
        )
    finally:
        session.close()


def test_factory_builds_explicit_production_runtime():
    session = Session()

    try:
        repositories = create_repository_set(
            session,
            mode=RuntimeRepositoryMode.PRODUCTION,
        )

        assert isinstance(
            repositories.episode,
            LegacyEpisodeRepository,
        )
        assert (
            repositories.episode
            is repositories.chapter
        )
    finally:
        session.close()


def test_factory_builds_shared_manga_runtime():
    session = Session()

    try:
        repositories = create_repository_set(
            session,
            mode=RuntimeRepositoryMode.SHARED_MANGA,
        )

        assert (
            repositories.mode
            is RuntimeRepositoryMode.SHARED_MANGA
        )
        assert isinstance(
            repositories.episode,
            SharedMangaEpisodeRepository,
        )
        assert isinstance(
            repositories.chapter,
            MangaRepository,
        )
        assert (
            repositories.episode
            is not repositories.chapter
        )
    finally:
        session.close()


def test_factory_rejects_unsupported_runtime_mode():
    session = Session()

    try:
        with pytest.raises(
            ValueError,
            match="Unsupported repository runtime mode",
        ):
            create_repository_set(
                session,
                mode="unknown",  # type: ignore[arg-type]
            )
    finally:
        session.close()
