from scraper.api.schemas import (
    EpisodeListResponse,
    EpisodeResponse,
)

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

@router.get("/{episode_number}", response_model=EpisodeResponse)
def get_episode_placeholder(
    episode_number: int,
):
    return {
        "id": 0,
        "anime_title": "Unknown",
        "episode_number": episode_number,
        "episode_title": None,
        "arc": None,
        "source_url": None,
    }