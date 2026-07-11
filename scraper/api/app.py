from fastapi import FastAPI

from scraper.api.routes.system import router as system_router
from scraper.api.routes.series import router as series_router
from scraper.api.routes.anime import router as anime_router
from scraper.api.routes.episodes import router as episode_router


app = FastAPI(
    title="AnimeMangaDB API",
)

app.include_router(system_router)
app.include_router(series_router)
app.include_router(anime_router)
app.include_router(episode_router)
