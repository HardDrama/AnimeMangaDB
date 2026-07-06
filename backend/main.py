from fastapi import FastAPI, HTTPException

from scraper.database.session import SessionLocal
from scraper.repositories.factory import create_episode_repository

from backend.models import AnimeResponse, EpisodeResponse, EpisodeChapterResponse

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AnimeMangaDB API",
    version="0.29.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
def search(query: str = ""):
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        anime_results = (
            repo.search_anime(query)
            if query.strip()
            else []
        )

        episode_results = (
            repo.search_episodes(query)
            if query.strip()
            else []
        )

        return {
            "query": query,
            "anime": [
                {
                    "id": anime.id,
                    "title": anime.title,
                    "provider": anime.provider,
                }
                for anime in anime_results
            ],
            "episodes": [
                {
                    "id": episode.id,
                    "anime_id": episode.anime_id,
                    "anime_title": repo.get_anime_by_id(
                        episode.anime_id
                    ).title,
                    "episode_number": episode.episode_number,
                    "title": episode.episode_title,
                    "arc": episode.arc,
                }
                for episode in episode_results
            ],
            "chapters": [],
        }

    finally:
        session.close()

@app.get("/anime", response_model=list[AnimeResponse])
def list_anime():
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        anime = repo.list_anime()

        return [
            AnimeResponse(
                id=item.id,
                title=item.title,
                provider=item.provider,
                episode_count=repo.count_episodes_for_anime(item.id),
            )
            for item in anime
        ]

    finally:
        session.close()

@app.get("/anime/{anime_id}", response_model=AnimeResponse)
def get_anime(anime_id: int):
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        anime = repo.get_anime_by_id(anime_id)

        if anime is None:
            raise HTTPException(
                status_code=404,
                detail="Anime not found",
            )

        return AnimeResponse(
            id=anime.id,
            title=anime.title,
            provider=anime.provider,
            episode_count=repo.count_episodes_for_anime(anime.id),
        )

    finally:
        session.close()

@app.get("/episodes", response_model=list[EpisodeResponse])
def list_episodes():
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        episodes = repo.list_episodes()

        return [
            EpisodeResponse(
                id=episode.id,
                anime_id=episode.anime_id,
                anime_title=repo.get_anime_by_id(episode.anime_id).title,
                episode_number=episode.episode_number,
                title=episode.episode_title,
                arc=episode.arc,
            )
            for episode in episodes
        ]

    finally:
        session.close()

@app.get("/episodes/{episode_id}", response_model=EpisodeResponse)
def get_episode(episode_id: int):
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        episode = repo.get_episode_by_id(episode_id)

        if episode is None:
            raise HTTPException(
                status_code=404,
                detail="Episode not found",
            )

        return EpisodeResponse(
            id=episode.id,
            anime_id=episode.anime_id,
            anime_title=repo.get_anime_by_id(episode.anime_id).title,
            episode_number=episode.episode_number,
            title=episode.episode_title,
            arc=episode.arc,
        )

    finally:
        session.close()

@app.get(
    "/anime/{anime_id}/episodes/{episode_number}",
    response_model=EpisodeResponse,
)
def get_episode_by_number(
    anime_id: int,
    episode_number: int,
):
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        episode = repo.get_episode_by_anime_and_number(
            anime_id=anime_id,
            episode_number=episode_number,
        )

        if episode is None:
            raise HTTPException(
                status_code=404,
                detail="Episode not found",
            )

        return EpisodeResponse(
            id=episode.id,
            anime_id=episode.anime_id,
            anime_title=repo.get_anime_by_id(episode.anime_id).title,
            episode_number=episode.episode_number,
            title=episode.episode_title,
            arc=episode.arc,
        )

    finally:
        session.close()

@app.get(
    "/episodes/{episode_id}/chapters",
    response_model=list[EpisodeChapterResponse],
)
def get_episode_chapters(episode_id: int):
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        chapters = repo.get_chapters_for_episode_id(episode_id)

        return [
            EpisodeChapterResponse(
                episode_id=chapter.episode_id,
                chapter_number=chapter.chapter_number,
            )
            for chapter in chapters
        ]

    finally:
        session.close()

@app.get(
    "/anime/{anime_id}/episodes",
    response_model=list[EpisodeResponse],
)
def list_episodes_for_anime(anime_id: int):
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        episodes = repo.list_episodes_for_anime(anime_id)

        return [
            EpisodeResponse(
                id=episode.id,
                anime_id=episode.anime_id,
                anime_title=repo.get_anime_by_id(episode.anime_id).title,
                episode_number=episode.episode_number,
                title=episode.episode_title,
                arc=episode.arc,
            )
            for episode in episodes
        ]

    finally:
        session.close()

@app.get(
    "/chapters/{chapter_number}/episodes",
    response_model=list[EpisodeResponse],
)
def get_episodes_by_chapter(chapter_number: int):
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        episodes = repo.get_episodes_by_chapter(chapter_number)

        return [
            EpisodeResponse(
                id=episode.id,
                anime_id=episode.anime_id,
                anime_title=repo.get_anime_by_id(episode.anime_id).title,
                episode_number=episode.episode_number,
                title=episode.episode_title,
                arc=episode.arc,
            )
            for episode in episodes
        ]

    finally:
        session.close()

@app.get("/")
def read_root():
    return {
        "message": "AnimeMangaDB API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "application": "AnimeMangaDB",
        "version": "0.29.0",
    }

@app.get("/version")
def version():
    return {
        "version": "0.29.0"
    }