from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from scraper.database.base import Base


class Anime(Base):
    __tablename__ = "anime"

    id: Mapped[int] = mapped_column(primary_key=True)

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

    episodes = relationship(
    "Episode",
    back_populates="anime",
    )

class Episode(Base):
    __tablename__ = "episodes"

    id: Mapped[int] = mapped_column(primary_key=True)

    anime_id: Mapped[int] = mapped_column(
        ForeignKey("anime.id"),
        nullable=False,
    )

    episode_number: Mapped[int] = mapped_column(nullable=False)

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

    anime = relationship("Anime", back_populates="episodes")

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class EpisodeChapter(Base):
    __tablename__ = "episode_chapters"

    id = Column(Integer, primary_key=True)

    episode_id = Column(Integer, ForeignKey("episodes.id"), nullable=False)

    chapter_number = Column(Integer, nullable=False)