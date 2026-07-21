from fastapi import APIRouter

from scraper.api.schemas import EpisodeResponse
from scraper.api.service_provider import build_api_service
from scraper.database.session import SessionLocal


router = APIRouter(
    prefix="/chapters",
    tags=["Chapters"],
)


@router.get(
    "/{chapter_number}/episodes",
    response_model=list[EpisodeResponse],
)
def get_episodes_for_chapter(chapter_number: int):
    session = SessionLocal()
    try:
        return build_api_service(
            session
        ).list_episodes_for_chapter(chapter_number)
    finally:
        session.close()
