from fastapi import APIRouter

router = APIRouter(
    prefix="/episodes",
    tags=["Episodes"],
)


@router.get("")
def list_episodes_placeholder():
    return {
        "episodes": [],
    }