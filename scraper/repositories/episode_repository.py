from sqlalchemy import select
from sqlalchemy.orm import Session

from scraper.database.models import (
    Anime,
    Episode,
    EpisodeChapter,
)
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
        existing = self.get_episode_by_number(
            anime,
            data.episode_number,
        )

        if existing:
            return existing
        
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
    
    def add_episode_chapters(
        self,
        episode: Episode,
        chapter_numbers: list[int],
    ):
        for chapter in chapter_numbers:
            if self.episode_has_chapter(
                episode,
                chapter,
            ):
                continue
            
            link = EpisodeChapter(
                episode_id=episode.id,
                chapter_number=chapter,
            )
            self.session.add(link)

        self.session.commit()

    def get_episode_by_number(
        self,
        anime: Anime,
        episode_number: int,
    ) -> Episode | None:

        stmt = (
            select(Episode)
            .where(Episode.anime_id == anime.id)
            .where(Episode.episode_number == episode_number)
        )

        return self.session.execute(stmt).scalar_one_or_none()
    
    def get_episode_by_source_url(
        self,
        source_url: str,
    ) -> Episode | None:

        stmt = (
            select(Episode)
            .where(Episode.source_url == source_url)
        )

        return self.session.execute(stmt).scalar_one_or_none()
    
    def episode_needs_update(
        self,
        episode: Episode,
        data: EpisodeData,
    ) -> bool:
        return (
            episode.episode_title != data.episode_title
            or episode.arc != data.arc
            or episode.source_url != str(data.source_url)
        )
    
    def episode_has_chapter(
        self,
        episode: Episode,
        chapter_number: int,
    ) -> bool:

        stmt = (
            select(EpisodeChapter)
            .where(EpisodeChapter.episode_id == episode.id)
            .where(EpisodeChapter.chapter_number == chapter_number)
        )

        return self.session.execute(stmt).scalar_one_or_none() is not None