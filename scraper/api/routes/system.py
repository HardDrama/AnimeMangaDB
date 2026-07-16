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
        "scope": "v3",
        "supported_scopes": [
            "v2",
            "v3",
        ],
        "compatibility": {
            "scope_v2": True,
        },
        "fields": {
            "anime": [
                "episode_number",
                "episode_title",
                "arc",
            ],
            "manga": [
                "chapter_number",
            ],
            "chapter_metadata": [
                "chapter_number",
                "chapter_title",
                "manga_arc",
                "source_url",
                "last_updated",
            ],
        },
    }

@router.get("/version")
def get_version():
    return {
        "api_version": "0.59.0",
        "platform_checkpoint": "v3 (certified)",
        "supported_scope": "v3",
        "scope_v2_compatible": True,
        "scope_v3_api_status": "certified",
    }