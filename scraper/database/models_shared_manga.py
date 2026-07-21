from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class SharedMangaBase(DeclarativeBase):
    """
    Isolated declarative base used to validate the shared-manga ORM
    contract before it replaces the production database models.

    This temporary base prevents duplicate SQLAlchemy table registration
    alongside the current production models during v0.64.15 preparation.
    """


class Manga(SharedMangaBase):
    __tablename__ = "manga"

    __table_args__ = (
        UniqueConstraint(
            "title",
            name="uq_manga_title",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    base_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    anime = relationship(
        "Anime",
        back_populates="manga",
    )

    chapters = relationship(
        "ChapterMetadata",
        back_populates="manga",
    )


class Anime(SharedMangaBase):
    __tablename__ = "anime"

    __table_args__ = (
        UniqueConstraint(
            "title",
            name="uq_anime_title",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    manga_id: Mapped[int] = mapped_column(
        ForeignKey("manga.id"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    base_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    manga = relationship(
        "Manga",
        back_populates="anime",
    )

    episodes = relationship(
        "Episode",
        back_populates="anime",
    )


class Episode(SharedMangaBase):
    __tablename__ = "episodes"

    __table_args__ = (
        UniqueConstraint(
            "anime_id",
            "episode_number",
            name="uq_episode_number",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    anime_id: Mapped[int] = mapped_column(
        ForeignKey("anime.id"),
        nullable=False,
    )

    episode_number: Mapped[int] = mapped_column(
        nullable=False,
    )

    episode_title: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    arc: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    source_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    last_updated: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    anime = relationship(
        "Anime",
        back_populates="episodes",
    )

    chapter_mappings = relationship(
        "EpisodeChapter",
        back_populates="episode",
    )


class EpisodeChapter(SharedMangaBase):
    __tablename__ = "episode_chapters"

    __table_args__ = (
        UniqueConstraint(
            "episode_id",
            "chapter_number",
            name="uq_episode_chapter",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    episode_id: Mapped[int] = mapped_column(
        ForeignKey("episodes.id"),
        nullable=False,
    )

    chapter_number: Mapped[int] = mapped_column(
        nullable=False,
    )

    episode = relationship(
        "Episode",
        back_populates="chapter_mappings",
    )


class ChapterMetadata(SharedMangaBase):
    __tablename__ = "chapter_metadata"

    __table_args__ = (
        UniqueConstraint(
            "manga_id",
            "chapter_number",
            name="uq_chapter_metadata_number",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    manga_id: Mapped[int] = mapped_column(
        ForeignKey("manga.id"),
        nullable=False,
        index=True,
    )

    chapter_number: Mapped[int] = mapped_column(
        nullable=False,
    )

    chapter_title: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    manga_arc: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    source_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    last_updated: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    manga = relationship(
        "Manga",
        back_populates="chapters",
    )