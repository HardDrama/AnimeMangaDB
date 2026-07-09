from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
    }


@router.get("/scope")
def get_scope():
    return {
        "scope": "v2",
        "fields": {
            "anime": [
                "episode_number",
                "episode_title",
                "arc",
            ],
            "manga": [
                "chapter_number",
            ],
        },
    }

@router.get("/version")
def get_version():
    return {
        "api_version": "0.52.0",
        "platform_checkpoint": "v2 (in progress)",
        "supported_scope": "v2",
    }