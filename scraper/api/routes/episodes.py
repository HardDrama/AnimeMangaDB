from scraper.api.schemas import EpisodeListResponse

from fastapi import APIRouter

router = APIRouter(
    prefix="/episodes",
    tags=["Episodes"],
)


@router.get("", response_model=EpisodeListResponse)
def list_episodes_placeholder():
    return {
        "episodes": [],
    }