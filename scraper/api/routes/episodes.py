from scraper.api.schemas import (
    EpisodeListResponse,
    EpisodeResponse,
)

from fastapi import APIRouter

from fastapi import HTTPException

from scraper.database.models import Episode
from scraper.database.session import SessionLocal

router = APIRouter(
    prefix="/episodes",
    tags=["Episodes"],
)


@router.get("", response_model=EpisodeListResponse)
def list_episodes_placeholder():
    return {
        "episodes": [],
    }

@router.get("/{episode_number}", response_model=EpisodeResponse)
def get_episode(
    episode_number: int,
):
    session = SessionLocal()

    try:
        episode = (
            session.query(Episode)
            .filter(
                Episode.episode_number == episode_number,
            )
            .first()
        )

        if episode is None:
            raise HTTPException(
                status_code=404,
                detail="Episode not found.",
            )

        return EpisodeResponse(
            id=episode.id,
            anime_title=episode.anime.title,
            episode_number=episode.episode_number,
            episode_title=episode.episode_title,
            arc=episode.arc,
            source_url=episode.source_url,
        )

    finally:
        session.close()