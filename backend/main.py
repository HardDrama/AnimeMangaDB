from fastapi import FastAPI

from scraper.database.session import SessionLocal
from scraper.repositories.factory import create_episode_repository

from backend.models import AnimeResponse, EpisodeResponse


app = FastAPI(
    title="AnimeMangaDB API",
    version="0.29.0",
)


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
            )
            for item in anime
        ]

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