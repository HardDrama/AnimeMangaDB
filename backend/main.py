from fastapi import FastAPI

from scraper.database.session import SessionLocal
from scraper.repositories.factory import create_episode_repository


app = FastAPI(
    title="AnimeMangaDB API",
    version="0.29.0",
)


@app.get("/anime")
def list_anime():
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        anime = repo.list_anime()

        return {
            "anime": [
                {
                    "id": item.id,
                    "title": item.title,
                    "provider": item.provider,
                }
                for item in anime
            ]
        }

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