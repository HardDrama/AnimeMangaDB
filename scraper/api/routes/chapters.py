from fastapi import APIRouter

from scraper.api.schemas import EpisodeResponse
from scraper.database.session import SessionLocal
from scraper.repositories.episode_repository import (
    EpisodeRepository,
)


router = APIRouter(
    prefix="/chapters",
    tags=["Chapters"],
)


@router.get(
    "/{chapter_number}/episodes",
    response_model=list[EpisodeResponse],
)
def get_episodes_for_chapter(
    chapter_number: int,
):
    session = SessionLocal()

    try:
        repository = EpisodeRepository(session)

        episodes = repository.get_episodes_by_chapter(
            chapter_number
        )

        return [
            EpisodeResponse(
                id=episode.id,
                anime_id=episode.anime_id,
                anime_title=episode.anime.title,
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