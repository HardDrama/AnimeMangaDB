from scraper.database.base import Base
from scraper.database.models import Anime
from scraper.models.episode import EpisodeData
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

def make_episode_data() -> EpisodeData:
    return EpisodeData(
        anime_title="One Piece",
        episode_number=1130,
        episode_title="Episode 1130",
        manga_start=1096,
        manga_end=1096,
        arc=None,
        source_url="https://onepiece.fandom.com/wiki/Episode_1130",
    )


def test_create_episode_creates_episode():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    episode = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    assert episode.id is not None
    assert episode.episode_number == 1130
    assert episode.episode_title == "Episode 1130"


def test_create_episode_reuses_existing_episode():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    first = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    second = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    assert first.id == second.id