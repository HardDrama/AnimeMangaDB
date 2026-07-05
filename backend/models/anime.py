from pydantic import BaseModel


class AnimeResponse(BaseModel):
    id: int
    title: str
    provider: str