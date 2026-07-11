from fastapi import APIRouter, HTTPException

from scraper.api.schemas import SeriesResponse
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
        )

    finally:
        session.close()