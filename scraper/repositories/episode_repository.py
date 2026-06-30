from sqlalchemy import select
from sqlalchemy.orm import Session

from scraper.database.models import Anime, Episode
from scraper.models.episode import EpisodeData


class EpisodeRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_or_create_anime(
        self,
        title: str,
        provider: str,
        base_url: str,
    ):
        stmt = select(Anime).where(Anime.title == title)
        result = self.session.execute(stmt).scalar_one_or_none()

        # If anime exists, return it
        if result:
            return result

        # Otherwise create it
        anime = Anime(
            title=title,
            provider=provider,
            base_url=base_url,
        )

        self.session.add(anime)
        self.session.commit()
        self.session.refresh(anime)

        return anime
    
    def create_episode(
        self,
        anime: Anime,
        data: EpisodeData,
    ):
        episode = Episode(
            anime_id=anime.id,
            episode_number=data.episode_number,
            episode_title=data.episode_title,
            arc=data.arc,
            source_url=str(data.source_url),
            last_updated=data.last_updated,
        )

        self.session.add(episode)
        self.session.commit()
        self.session.refresh(episode)

        return episode