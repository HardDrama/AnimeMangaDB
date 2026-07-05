from fastapi import FastAPI


app = FastAPI(
    title="AnimeMangaDB API",
    version="0.29.0",
)


@app.get("/")
def read_root():
    return {
        "message": "AnimeMangaDB API is running"
    }