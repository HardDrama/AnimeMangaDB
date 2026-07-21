from fastapi import APIRouter, HTTPException

from scraper.api.schemas import (
    ArcSummaryResponse,
    ChapterMetadataResponse,
    EpisodeResponse,
    SeriesResponse,
)
from scraper.api.service_provider import build_api_service
from scraper.database.session import SessionLocal


router = APIRouter(
    prefix="/anime",
    tags=["Anime Compatibility"],
)


@router.get("", response_model=list[SeriesResponse])
def list_anime():
    session = SessionLocal()
    try:
        return build_api_service(session).list_series()
    finally:
        session.close()


@router.get("/{anime_id}", response_model=SeriesResponse)
def get_anime(anime_id: int):
    session = SessionLocal()
    try:
        result = build_api_service(session).get_series(anime_id)
        if result is None:
            raise HTTPException(404, "Anime not found.")
        return result
    finally:
        session.close()


@router.get(
    "/{anime_id}/arcs",
    response_model=list[ArcSummaryResponse],
)
def list_arcs_for_anime(anime_id: int):
    session = SessionLocal()
    try:
        result = build_api_service(session).list_arcs_for_anime(
            anime_id
        )
        if result is None:
            raise HTTPException(404, "Anime not found.")
        return result
    finally:
        session.close()


@router.get(
    "/{anime_id}/episodes",
    response_model=list[EpisodeResponse],
)
def list_episodes_for_anime(anime_id: int):
    session = SessionLocal()
    try:
        result = build_api_service(
            session
        ).list_episodes_for_anime(anime_id)
        if result is None:
            raise HTTPException(404, "Anime not found.")
        return result
    finally:
        session.close()


@router.get(
    "/{anime_id}/chapters",
    response_model=list[ChapterMetadataResponse],
)
def list_chapters_for_anime(anime_id: int):
    session = SessionLocal()
    try:
        result = build_api_service(
            session
        ).list_chapters_for_anime(anime_id)
        if result is None:
            raise HTTPException(404, "Anime not found.")
        return result
    finally:
        session.close()


@router.get(
    "/{anime_id}/chapters/{chapter_number}",
    response_model=ChapterMetadataResponse,
)
def get_chapter_for_anime(
    anime_id: int,
    chapter_number: int,
):
    session = SessionLocal()
    try:
        service = build_api_service(session)

        if service.get_series(anime_id) is None:
            raise HTTPException(404, "Anime not found.")

        result = service.get_chapter_for_anime(
            anime_id=anime_id,
            chapter_number=chapter_number,
        )
        if result is None:
            raise HTTPException(404, "Chapter not found.")

        return result
    finally:
        session.close()


@router.get(
    "/{anime_id}/chapters/{chapter_number}/episodes",
    response_model=list[EpisodeResponse],
)
def list_episodes_for_chapter(
    anime_id: int,
    chapter_number: int,
):
    session = SessionLocal()
    try:
        service = build_api_service(session)

        if service.get_series(anime_id) is None:
            raise HTTPException(404, "Anime not found.")

        result = service.list_episodes_for_anime_chapter(
            anime_id=anime_id,
            chapter_number=chapter_number,
        )
        if result is None:
            raise HTTPException(404, "Chapter not found.")

        return result
    finally:
        session.close()
