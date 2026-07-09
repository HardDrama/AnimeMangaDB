from pydantic import BaseModel


class EpisodeResponse(BaseModel):
    id: int
    anime_title: str
    episode_number: int
    episode_title: str | None = None
    arc: str | None = None
    source_url: str | None = None