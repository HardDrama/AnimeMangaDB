from pydantic import BaseModel


class EpisodeResponse(BaseModel):
    id: int
    anime_id: int
    anime_title: str
    episode_number: int
    title: str
    arc: str | None = None