from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scraper.api.routes.system import router as system_router
from scraper.api.routes.series import router as series_router
from scraper.api.routes.anime import router as anime_router
from scraper.api.routes.episodes import router as episode_router
from scraper.api.routes.search import router as search_router
from scraper.api.routes.chapters import router as chapter_router


app = FastAPI(
    title="AnimeMangaDB API",
)

app = FastAPI(
    title="AnimeMangaDB API",
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

app.include_router(system_router)
app.include_router(series_router)
app.include_router(anime_router)
app.include_router(episode_router)
app.include_router(search_router)
app.include_router(chapter_router)