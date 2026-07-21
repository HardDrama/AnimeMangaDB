from sqlalchemy import (
    delete,
    func,
    or_,
    select,
)
from sqlalchemy.orm import Session

from scraper.database.models_shared_manga import (
    Anime,
    Episode,
    EpisodeChapter,
)
from scraper.models.episode import EpisodeData


class EpisodeRepository:
    """
    Shared-manga runtime candidate for anime, episode, and
    episode-to-chapter mapping operations.

    This staged repository intentionally excludes Manga and
    ChapterMetadata persistence. Those responsibilities belong to
    MangaRepository.
    """

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def normalize_arc_name(
        value: str,
    ) -> str:
        normalized = value.strip()

        if normalized.casefold().endswith(" arc"):
            normalized = normalized[:-4].strip()

        return normalized.casefold()

    def get_or_create_anime(
        self,
        title: str,
        provider: str,
        base_url: str,
        manga_id: int,
    ) -> Anime:
        stmt = select(Anime).where(
            Anime.title == title
        )
        result = (
            self.session.execute(stmt)
            .scalar_one_or_none()
        )

        if result is not None:
            if result.manga_id != manga_id:
                result.manga_id = manga_id
                self.session.commit()
                self.session.refresh(result)

            return result

        anime = Anime(
            title=title,
            provider=provider,
            base_url=base_url,
            manga_id=manga_id,
        )

        self.session.add(anime)
        self.session.commit()
        self.session.refresh(anime)

        return anime

    def create_episode(
        self,
        anime: Anime,
        data: EpisodeData,
    ) -> Episode:
        existing = self.get_episode_by_number(
            anime,
            data.episode_number,
        )

        if existing is not None:
            if self.episode_needs_update(
                episode=existing,
                data=data,
            ):
                return self.update_episode(
                    episode=existing,
                    data=data,
                )

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

    def get_chapter_numbers_for_episode(
        self,
        episode: Episode,
    ) -> list[int]:
        stmt = (
            select(EpisodeChapter.chapter_number)
            .where(
                EpisodeChapter.episode_id
                == episode.id
            )
        )

        result = (
            self.session.execute(stmt)
            .scalars()
            .all()
        )

        return sorted(result)

    def chapter_mappings_need_update(
        self,
        episode: Episode,
        chapter_numbers: list[int],
    ) -> bool:
        existing_chapters = (
            self.get_chapter_numbers_for_episode(
                episode
            )
        )

        return existing_chapters != sorted(
            chapter_numbers
        )

    def replace_episode_chapters(
        self,
        episode: Episode,
        chapter_numbers: list[int],
    ) -> None:
        stmt = delete(EpisodeChapter).where(
            EpisodeChapter.episode_id
            == episode.id
        )

        self.session.execute(stmt)
        self.session.commit()

        self.add_episode_chapters(
            episode=episode,
            chapter_numbers=chapter_numbers,
        )

    def add_episode_chapters(
        self,
        episode: Episode,
        chapter_numbers: list[int],
    ) -> None:
        for chapter_number in chapter_numbers:
            if self.episode_has_chapter(
                episode,
                chapter_number,
            ):
                continue

            self.session.add(
                EpisodeChapter(
                    episode_id=episode.id,
                    chapter_number=chapter_number,
                )
            )

        self.session.commit()

    def list_episode_arc_summaries(
        self,
        anime_id: int,
    ) -> list[dict]:
        rows = self.session.execute(
            select(
                Episode.arc,
                func.count(Episode.id),
                func.min(
                    Episode.episode_number
                ),
            )
            .where(Episode.anime_id == anime_id)
            .where(Episode.arc.is_not(None))
            .where(func.trim(Episode.arc) != "")
            .group_by(Episode.arc)
            .order_by(
                func.min(
                    Episode.episode_number
                )
            )
        ).all()

        return [
            {
                "name": arc.strip(),
                "episode_arc": arc.strip(),
                "manga_arc": None,
                "episode_count": count,
                "chapter_count": 0,
                "first_episode": first_episode,
            }
            for arc, count, first_episode in rows
        ]

    def get_episode_by_number(
        self,
        anime: Anime,
        episode_number: int,
    ) -> Episode | None:
        stmt = (
            select(Episode)
            .where(Episode.anime_id == anime.id)
            .where(
                Episode.episode_number
                == episode_number
            )
        )

        return (
            self.session.execute(stmt)
            .scalar_one_or_none()
        )

    def get_episode_by_source_url(
        self,
        source_url: str,
    ) -> Episode | None:
        stmt = select(Episode).where(
            Episode.source_url == source_url
        )

        return (
            self.session.execute(stmt)
            .scalar_one_or_none()
        )

    def episode_needs_update(
        self,
        episode: Episode,
        data: EpisodeData,
    ) -> bool:
        return (
            episode.episode_title
            != data.episode_title
            or episode.arc != data.arc
            or episode.source_url
            != str(data.source_url)
        )

    def update_episode(
        self,
        episode: Episode,
        data: EpisodeData,
    ) -> Episode:
        episode.episode_title = data.episode_title
        episode.arc = data.arc
        episode.source_url = str(data.source_url)
        episode.last_updated = data.last_updated

        self.session.commit()
        self.session.refresh(episode)

        return episode

    def episode_has_chapter(
        self,
        episode: Episode,
        chapter_number: int,
    ) -> bool:
        stmt = (
            select(EpisodeChapter)
            .where(
                EpisodeChapter.episode_id
                == episode.id
            )
            .where(
                EpisodeChapter.chapter_number
                == chapter_number
            )
        )

        return (
            self.session.execute(stmt)
            .scalar_one_or_none()
            is not None
        )

    def list_anime(self) -> list[Anime]:
        return (
            self.session.query(Anime)
            .order_by(Anime.title)
            .all()
        )

    def list_episodes(self) -> list[Episode]:
        return (
            self.session.query(Episode)
            .order_by(Episode.episode_number)
            .all()
        )

    def get_anime_by_id(
        self,
        anime_id: int,
    ) -> Anime | None:
        return self.session.get(
            Anime,
            anime_id,
        )

    def get_anime_by_title(
        self,
        title: str,
    ) -> Anime | None:
        stmt = select(Anime).where(
            Anime.title == title
        )

        return (
            self.session.execute(stmt)
            .scalar_one_or_none()
        )

    def get_episode_by_id(
        self,
        episode_id: int,
    ) -> Episode | None:
        return self.session.get(
            Episode,
            episode_id,
        )

    def get_episode_by_anime_and_number(
        self,
        anime_id: int,
        episode_number: int,
    ) -> Episode | None:
        stmt = (
            select(Episode)
            .where(Episode.anime_id == anime_id)
            .where(
                Episode.episode_number
                == episode_number
            )
        )

        return (
            self.session.execute(stmt)
            .scalar_one_or_none()
        )

    def get_chapters_for_episode_id(
        self,
        episode_id: int,
    ) -> list[EpisodeChapter]:
        stmt = (
            select(EpisodeChapter)
            .where(
                EpisodeChapter.episode_id
                == episode_id
            )
            .order_by(
                EpisodeChapter.chapter_number
            )
        )

        return (
            self.session.execute(stmt)
            .scalars()
            .all()
        )

    def count_episodes_for_anime(
        self,
        anime_id: int,
    ) -> int:
        return (
            self.session.query(Episode)
            .where(Episode.anime_id == anime_id)
            .count()
        )

    def list_episodes_for_anime(
        self,
        anime_id: int,
    ) -> list[Episode]:
        return (
            self.session.query(Episode)
            .where(Episode.anime_id == anime_id)
            .order_by(Episode.episode_number)
            .all()
        )

    def get_episodes_by_chapter(
        self,
        chapter_number: int,
    ) -> list[Episode]:
        stmt = (
            select(Episode)
            .join(EpisodeChapter)
            .where(
                EpisodeChapter.chapter_number
                == chapter_number
            )
            .order_by(
                Episode.anime_id,
                Episode.episode_number,
            )
        )

        return (
            self.session.execute(stmt)
            .scalars()
            .all()
        )

    def get_episodes_by_anime_and_chapter(
        self,
        anime_id: int,
        chapter_number: int,
    ) -> list[Episode]:
        stmt = (
            select(Episode)
            .join(EpisodeChapter)
            .where(Episode.anime_id == anime_id)
            .where(
                EpisodeChapter.chapter_number
                == chapter_number
            )
            .order_by(Episode.episode_number)
        )

        return (
            self.session.execute(stmt)
            .scalars()
            .all()
        )

    def search_anime(
        self,
        query: str,
    ) -> list[Anime]:
        return (
            self.session.query(Anime)
            .where(
                Anime.title.ilike(
                    f"%{query}%"
                )
            )
            .order_by(Anime.title)
            .all()
        )

    def search_episodes(
        self,
        query: str,
    ) -> list[Episode]:
        filters = [
            Episode.episode_title.ilike(
                f"%{query}%"
            ),
            Episode.arc.ilike(
                f"%{query}%"
            ),
        ]

        try:
            episode_number = int(query)
            filters.append(
                Episode.episode_number
                == episode_number
            )
        except ValueError:
            pass

        return (
            self.session.query(Episode)
            .where(or_(*filters))
            .order_by(
                Episode.anime_id,
                Episode.episode_number,
            )
            .all()
        )
