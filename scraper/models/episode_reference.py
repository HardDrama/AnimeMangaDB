from pydantic import BaseModel


class EpisodeReference(BaseModel):
    episode_number: int
    url: str