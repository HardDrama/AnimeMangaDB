from fastapi import APIRouter, Query

from scraper.api.schemas import (
    ChapterMetadataResponse,
    ChapterSearchResult,
    EpisodeResponse,
    SearchResponse,
    SeriesResponse,
)
from scraper.database.session import SessionLocal
from scraper.repositories.episode_repository import (
    EpisodeRepository,
)


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
        repository = EpisodeRepository(session)

        anime_results = repository.search_anime(
            query
        )

        episode_results = repository.search_episodes(
            query
        )

        chapter_metadata_results = (
            repository.search_chapter_metadata(
                query
            )
        )

        chapter_results = []

        try:
            chapter_number = int(query)

            chapter_episodes = (
                repository.get_episodes_by_chapter(
                    chapter_number
                )
            )

            if chapter_episodes:
                chapter_results.append(
                    ChapterSearchResult(
                        chapter_number=chapter_number,
                        episodes=[
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
                            for episode in chapter_episodes
                        ],
                    )
                )

        except ValueError:
            pass

        return SearchResponse(
            anime=[
                SeriesResponse(
                    id=anime.id,
                    title=anime.title,
                    provider=anime.provider,
                    base_url=anime.base_url,
                    episode_count=(
                        repository.count_episodes_for_anime(
                            anime.id
                        )
                    ),
                )
                for anime in anime_results
            ],
            episodes=[
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
                for episode in episode_results
            ],
            chapters=chapter_results,
            chapter_metadata=[
                ChapterMetadataResponse
                .model_validate(
                    chapter
                )
                for chapter in (
                    chapter_metadata_results
                )
            ],
        )

    finally:
        session.close()