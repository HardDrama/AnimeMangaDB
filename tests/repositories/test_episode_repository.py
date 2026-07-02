from scraper.database.base import Base
from scraper.database.models import Anime
from scraper.database.models import EpisodeChapter
from scraper.models.episode import EpisodeData
from scraper.repositories.episode_repository import EpisodeRepository

from sqlalchemy import create_engine
from sqlalchemy import select
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

def test_add_episode_chapters_creates_chapter_link():
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

    repo.add_episode_chapters(
        episode=episode,
        chapter_numbers=[1096],
    )

    stmt = select(EpisodeChapter).where(
        EpisodeChapter.episode_id == episode.id
    )

    chapters = session.execute(stmt).scalars().all()

    assert len(chapters) == 1
    assert chapters[0].chapter_number == 1096


def test_add_episode_chapters_does_not_duplicate_links():
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

    repo.add_episode_chapters(
        episode=episode,
        chapter_numbers=[1096],
    )

    repo.add_episode_chapters(
        episode=episode,
        chapter_numbers=[1096],
    )

    stmt = select(EpisodeChapter).where(
        EpisodeChapter.episode_id == episode.id
    )

    chapters = session.execute(stmt).scalars().all()

    assert len(chapters) == 1