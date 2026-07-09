from fastapi import FastAPI

from scraper.api.routes.system import router as system_router


app = FastAPI(
    title="AnimeMangaDB API",
)

app.include_router(system_router)