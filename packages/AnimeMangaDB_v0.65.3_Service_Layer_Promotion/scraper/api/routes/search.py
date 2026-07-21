from fastapi import APIRouter, Query

from scraper.api.schemas import SearchResponse
from scraper.api.service_provider import build_api_service
from scraper.database.session import SessionLocal


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.get("", response_model=SearchResponse)
def search_database(
    query: str = Query(min_length=1),
):
    session = SessionLocal()
    try:
        return build_api_service(session).search(query)
    finally:
        session.close()
