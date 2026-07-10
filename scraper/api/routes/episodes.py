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
def list_episodes(
    limit: int = 25,
    offset: int = 0,
):
    session = SessionLocal()

    try:
        episodes = (
            session.query(Episode)
            .order_by(Episode.episode_number)
            .offset(offset)
            .limit(limit)
            .all()
        )

        return EpisodeListResponse(
            episodes=[
                EpisodeResponse(
                    id=episode.id,
                    anime_title=episode.anime.title,
                    episode_number=episode.episode_number,
                    episode_title=episode.episode_title,
                    arc=episode.arc,
                    source_url=episode.source_url,
                )
                for episode in episodes
            ]
        )

    finally:
        session.close()

@router.get("/count")
def get_episode_count():
    session = SessionLocal()

    try:
        count = session.query(Episode).count()

        return {
            "episode_count": count,
        }

    finally:
        session.close()

@router.get("/id/{episode_id}", response_model=EpisodeResponse)
def get_episode_by_id(
    episode_id: int,
):
    session = SessionLocal()

    try:
        episode = (
            session.query(Episode)
            .filter(Episode.id == episode_id)
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