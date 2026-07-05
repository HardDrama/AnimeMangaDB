from fastapi import FastAPI


app = FastAPI(
    title="AnimeMangaDB API",
    version="0.29.0",
)


@app.get("/anime")
def list_anime():
    return {
        "anime": []
    }

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