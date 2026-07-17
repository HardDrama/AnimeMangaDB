from fastapi import APIRouter, HTTPException

from scraper.api.schemas import (
    ChapterMetadataResponse,
    EpisodeResponse,
    SeriesResponse,
)
from scraper.database.session import SessionLocal
from scraper.repositories.episode_repository import (
    EpisodeRepository,
)


router = APIRouter(
    prefix="/anime",
    tags=["Anime Compatibility"],
)


@router.get("", response_model=list[SeriesResponse])
def list_anime():
    session = SessionLocal()

    try:
        repository = EpisodeRepository(session)

        anime_list = repository.list_anime()

        return [
            SeriesResponse(
                id=anime.id,
                title=anime.title,
                provider=anime.provider,
                base_url=anime.base_url,
                episode_count=repository.count_episodes_for_anime(
                    anime.id
                ),
                chapter_count=(
                    repository.count_chapters_for_anime(
                        anime.id
                    )
                ),
            )
            for anime in anime_list
        ]

    finally:
        session.close()


@router.get(
    "/{anime_id}",
    response_model=SeriesResponse,
)
def get_anime(
    anime_id: int,
):
    session = SessionLocal()

    try:
        repository = EpisodeRepository(session)

        anime = repository.get_anime_by_id(
            anime_id
        )

        if anime is None:
            raise HTTPException(
                status_code=404,
                detail="Anime not found.",
            )

        return SeriesResponse(
            id=anime.id,
            title=anime.title,
            provider=anime.provider,
            base_url=anime.base_url,
            episode_count=repository.count_episodes_for_anime(
                anime.id
            ),
            chapter_count=(
                repository.count_chapters_for_anime(
                    anime.id
                )
            ),
        )

    finally:
        session.close()

@router.get(
    "/{anime_id}/episodes",
    response_model=list[EpisodeResponse],
)
def list_episodes_for_anime(
    anime_id: int,
):
    session = SessionLocal()

    try:
        repository = EpisodeRepository(session)

        anime = repository.get_anime_by_id(
            anime_id
        )

        if anime is None:
            raise HTTPException(
                status_code=404,
                detail="Anime not found.",
            )

        episodes = repository.list_episodes_for_anime(
            anime_id
        )

        return [
            EpisodeResponse(
                id=episode.id,
                anime_id=episode.anime_id,
                anime_title=anime.title,
                episode_number=episode.episode_number,
                episode_title=episode.episode_title,
                title=episode.episode_title,
                arc=episode.arc,
                source_url=episode.source_url,
            )
            for episode in episodes
        ]

    finally:
        session.close()

@router.get(
    "/{anime_id}/chapters",
    response_model=list[
        ChapterMetadataResponse
    ],
)
def list_chapters_for_anime(
    anime_id: int,
):
    session = SessionLocal()

    try:
        repository = EpisodeRepository(
            session
        )

        anime = repository.get_anime_by_id(
            anime_id
        )

        if anime is None:
            raise HTTPException(
                status_code=404,
                detail="Anime not found.",
            )

        chapters = (
            repository.list_chapter_metadata(
                anime_id
            )
        )

        return [
            ChapterMetadataResponse.model_validate(
                chapter
            )
            for chapter in chapters
        ]

    finally:
        session.close()

@router.get(
    "/{anime_id}/chapters/{chapter_number}",
    response_model=ChapterMetadataResponse,
)
def get_chapter_for_anime(
    anime_id: int,
    chapter_number: int,
):
    session = SessionLocal()

    try:
        repository = EpisodeRepository(
            session
        )

        anime = repository.get_anime_by_id(
            anime_id
        )

        if anime is None:
            raise HTTPException(
                status_code=404,
                detail="Anime not found.",
            )

        chapter = repository.get_chapter_metadata(
            anime_id=anime_id,
            chapter_number=chapter_number,
        )

        if chapter is None:
            raise HTTPException(
                status_code=404,
                detail="Chapter not found.",
            )

        return (
            ChapterMetadataResponse
            .model_validate(
                chapter
            )
        )

    finally:
        session.close()

@router.get(
    (
        "/{anime_id}/chapters/"
        "{chapter_number}/episodes"
    ),
    response_model=list[
        EpisodeResponse
    ],
)
def list_episodes_for_chapter(
    anime_id: int,
    chapter_number: int,
):
    session = SessionLocal()

    try:
        repository = EpisodeRepository(
            session
        )

        anime = repository.get_anime_by_id(
            anime_id
        )

        if anime is None:
            raise HTTPException(
                status_code=404,
                detail="Anime not found.",
            )

        chapter = (
            repository.get_chapter_metadata(
                anime_id=anime_id,
                chapter_number=(
                    chapter_number
                ),
            )
        )

        if chapter is None:
            raise HTTPException(
                status_code=404,
                detail="Chapter not found.",
            )

        episodes = (
            repository
            .get_episodes_by_anime_and_chapter(
                anime_id=anime_id,
                chapter_number=(
                    chapter_number
                ),
            )
        )

        return [
            EpisodeResponse(
                id=episode.id,
                anime_id=episode.anime_id,
                anime_title=anime.title,
                episode_number=(
                    episode.episode_number
                ),
                episode_title=(
                    episode.episode_title
                ),
                title=(
                    episode.episode_title
                ),
                arc=episode.arc,
                source_url=(
                    episode.source_url
                ),
            )
            for episode in episodes
        ]

    finally:
        session.close()