from pydantic import BaseModel


class EpisodeChapterResponse(BaseModel):
    episode_id: int
    chapter_number: int