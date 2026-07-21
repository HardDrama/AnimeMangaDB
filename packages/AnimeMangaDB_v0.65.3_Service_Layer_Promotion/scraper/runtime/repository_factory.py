from dataclasses import dataclass
from enum import Enum

from sqlalchemy.orm import Session

from scraper.runtime.repository_provider import RuntimeRepositoryProvider


class RuntimeRepositoryMode(str, Enum):
    PRODUCTION = "production"
    SHARED_MANGA = "shared_manga"


@dataclass(frozen=True)
class RuntimeRepositorySet:
    episode: object
    chapter: object
    mode: RuntimeRepositoryMode


def create_repository_set(
    session: Session,
    mode: RuntimeRepositoryMode = RuntimeRepositoryMode.PRODUCTION,
) -> RuntimeRepositorySet:
    """
    Build a compatible episode and manga repository pair.
    """

    if mode is RuntimeRepositoryMode.PRODUCTION:
        episode_repository = (
            RuntimeRepositoryProvider
            .production_episode_repository(session)
        )
        chapter_repository = (
            RuntimeRepositoryProvider
            .production_chapter_repository(session)
        )

        return RuntimeRepositorySet(
            episode=episode_repository,
            chapter=chapter_repository,
            mode=mode,
        )

    if mode is RuntimeRepositoryMode.SHARED_MANGA:
        episode_repository = (
            RuntimeRepositoryProvider
            .staged_episode_repository(session)
        )
        chapter_repository = (
            RuntimeRepositoryProvider
            .staged_chapter_repository(session)
        )

        return RuntimeRepositorySet(
            episode=episode_repository,
            chapter=chapter_repository,
            mode=mode,
        )

    raise ValueError(
        f"Unsupported repository runtime mode: {mode!r}"
    )
