from pydantic import BaseModel


class EpisodeResponse(BaseModel):
    id: int
    anime_id: int
    episode_number: int
    title: str
    arc: str | None