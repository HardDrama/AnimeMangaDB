from fastapi import APIRouter

from scraper.api.schemas import (
    SeriesListResponse,
    SeriesResponse,
)
from scraper.database.models import Anime
from scraper.database.session import SessionLocal


router = APIRouter(
    prefix="/series",
    tags=["Series"],
)


@router.get("", response_model=SeriesListResponse)
def list_series():
    session = SessionLocal()

    try:
        anime_list = (
            session.query(Anime)
            .order_by(Anime.title)
            .all()
        )

        return SeriesListResponse(
            series=[
                SeriesResponse(
                    id=anime.id,
                    title=anime.title,
                    provider=anime.provider,
                    base_url=anime.base_url,
                )
                for anime in anime_list
            ]
        )

    finally:
        session.close()