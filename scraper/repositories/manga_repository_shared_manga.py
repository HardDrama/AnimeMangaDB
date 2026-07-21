from sqlalchemy import (
    func,
    or_,
    select,
)
from sqlalchemy.orm import Session

from scraper.database.models_shared_manga import (
    Anime,
    ChapterMetadata,
    Manga,
)
from scraper.models.chapter_metadata import (
    ChapterMetadata as ChapterMetadataData,
)


class MangaRepository:
    """
    Shared-manga runtime candidate for Manga and ChapterMetadata
    persistence and lookup.
    """

    _CANONICAL_MANGA_TITLES = {
        "Naruto Shippuden": "Naruto",
    }

    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def canonical_manga_title(
        cls,
        anime_title: str,
    ) -> str:
        return cls._CANONICAL_MANGA_TITLES.get(
            anime_title,
            anime_title,
        )

    @staticmethod
    def normalize_arc_name(
        value: str,
    ) -> str:
        normalized = value.strip()

        if normalized.casefold().endswith(" arc"):
            normalized = normalized[:-4].strip()

        return normalized.casefold()

    def get_manga_by_id(
        self,
        manga_id: int,
    ) -> Manga | None:
        return self.session.get(
            Manga,
            manga_id,
        )

    def get_manga_by_title(
        self,
        title: str,
    ) -> Manga | None:
        stmt = select(Manga).where(
            Manga.title == title
        )

        return (
            self.session.execute(stmt)
            .scalar_one_or_none()
        )

    def get_or_create_manga(
        self,
        title: str,
        provider: str,
        base_url: str,
    ) -> Manga:
        canonical_title = (
            self.canonical_manga_title(title)
        )

        manga = self.get_manga_by_title(
            canonical_title
        )

        if manga is not None:
            return manga

        manga = Manga(
            title=canonical_title,
            provider=provider,
            base_url=base_url,
        )

        self.session.add(manga)
        self.session.commit()
        self.session.refresh(manga)

        return manga

    def get_manga_for_anime(
        self,
        anime: Anime,
    ) -> Manga:
        manga = anime.manga

        if manga is None:
            raise RuntimeError(
                f"Anime '{anime.title}' has no manga assignment."
            )

        return manga

    def get_chapter_metadata(
        self,
        manga_id: int,
        chapter_number: int,
    ) -> ChapterMetadata | None:
        stmt = (
            select(ChapterMetadata)
            .where(
                ChapterMetadata.manga_id
                == manga_id
            )
            .where(
                ChapterMetadata.chapter_number
                == chapter_number
            )
        )

        return (
            self.session.execute(stmt)
            .scalar_one_or_none()
        )

    def get_chapter_metadata_for_anime(
        self,
        anime: Anime,
        chapter_number: int,
    ) -> ChapterMetadata | None:
        return self.get_chapter_metadata(
            manga_id=anime.manga_id,
            chapter_number=chapter_number,
        )

    def create_or_update_chapter_metadata(
        self,
        manga: Manga,
        chapter_number: int,
        chapter_title: str | None = None,
        manga_arc: str | None = None,
        source_url: str | None = None,
        last_updated=None,
    ) -> ChapterMetadata:
        chapter = self.get_chapter_metadata(
            manga_id=manga.id,
            chapter_number=chapter_number,
        )

        if chapter is None:
            chapter = ChapterMetadata(
                manga_id=manga.id,
                chapter_number=chapter_number,
                chapter_title=chapter_title,
                manga_arc=manga_arc,
                source_url=source_url,
                last_updated=last_updated,
            )

            self.session.add(chapter)
        else:
            chapter.chapter_title = chapter_title
            chapter.manga_arc = manga_arc
            chapter.source_url = source_url
            chapter.last_updated = last_updated

        self.session.commit()
        self.session.refresh(chapter)

        return chapter

    def save_chapter_metadata(
        self,
        manga: Manga,
        metadata: ChapterMetadataData,
    ) -> ChapterMetadata:
        return self.create_or_update_chapter_metadata(
            manga=manga,
            chapter_number=metadata.chapter_number,
            chapter_title=metadata.chapter_title,
            manga_arc=metadata.manga_arc,
            source_url=metadata.source_url,
            last_updated=metadata.last_updated,
        )

    def save_chapter_metadata_for_anime(
        self,
        anime: Anime,
        metadata: ChapterMetadataData,
    ) -> ChapterMetadata:
        manga = self.get_manga_for_anime(anime)

        return self.save_chapter_metadata(
            manga=manga,
            metadata=metadata,
        )

    def list_chapter_metadata(
        self,
        manga_id: int,
    ) -> list[ChapterMetadata]:
        stmt = (
            select(ChapterMetadata)
            .where(
                ChapterMetadata.manga_id
                == manga_id
            )
            .order_by(
                ChapterMetadata.chapter_number
            )
        )

        return (
            self.session.execute(stmt)
            .scalars()
            .all()
        )

    def list_chapter_metadata_for_anime(
        self,
        anime: Anime,
    ) -> list[ChapterMetadata]:
        return self.list_chapter_metadata(
            manga_id=anime.manga_id
        )

    def count_chapters_for_manga(
        self,
        manga_id: int,
    ) -> int:
        return (
            self.session.query(ChapterMetadata)
            .where(
                ChapterMetadata.manga_id
                == manga_id
            )
            .count()
        )

    def count_chapters_for_anime(
        self,
        anime: Anime,
    ) -> int:
        return self.count_chapters_for_manga(
            manga_id=anime.manga_id
        )

    def list_manga_arc_summaries(
        self,
        manga_id: int,
    ) -> list[dict]:
        rows = self.session.execute(
            select(
                ChapterMetadata.manga_arc,
                func.count(
                    ChapterMetadata.chapter_number
                ),
                func.min(
                    ChapterMetadata.chapter_number
                ),
            )
            .where(
                ChapterMetadata.manga_id
                == manga_id
            )
            .where(
                ChapterMetadata.manga_arc
                .is_not(None)
            )
            .where(
                func.trim(
                    ChapterMetadata.manga_arc
                ) != ""
            )
            .group_by(
                ChapterMetadata.manga_arc
            )
            .order_by(
                func.min(
                    ChapterMetadata.chapter_number
                )
            )
        ).all()

        return [
            {
                "name": (
                    manga_arc[:-4].strip()
                    if manga_arc.casefold().endswith(
                        " arc"
                    )
                    else manga_arc.strip()
                ),
                "episode_arc": None,
                "manga_arc": manga_arc.strip(),
                "episode_count": 0,
                "chapter_count": chapter_count,
                "first_chapter": first_chapter,
            }
            for (
                manga_arc,
                chapter_count,
                first_chapter,
            ) in rows
        ]

    def search_chapter_metadata(
        self,
        query: str,
    ) -> list[ChapterMetadata]:
        filters = [
            ChapterMetadata.chapter_title.ilike(
                f"%{query}%"
            ),
            ChapterMetadata.manga_arc.ilike(
                f"%{query}%"
            ),
        ]

        try:
            chapter_number = int(query)
            filters.append(
                ChapterMetadata.chapter_number
                == chapter_number
            )
        except ValueError:
            pass

        stmt = (
            select(ChapterMetadata)
            .where(or_(*filters))
            .order_by(
                ChapterMetadata.manga_id,
                ChapterMetadata.chapter_number,
            )
        )

        return (
            self.session.execute(stmt)
            .scalars()
            .all()
        )
