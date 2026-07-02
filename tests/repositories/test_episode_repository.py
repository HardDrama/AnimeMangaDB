from scraper.database.base import Base
from scraper.database.models import Anime
from scraper.repositories.episode_repository import EpisodeRepository

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_test_session():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    TestingSession = sessionmaker(bind=engine)

    return TestingSession()


def test_get_or_create_anime_creates_anime():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    assert anime.id is not None
    assert anime.title == "One Piece"


def test_get_or_create_anime_reuses_existing_anime():
    session = create_test_session()
    repo = EpisodeRepository(session)

    first = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    second = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    assert first.id == second.id