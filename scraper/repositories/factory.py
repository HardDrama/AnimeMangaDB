from sqlalchemy.orm import Session

from scraper.repositories.episode_repository import EpisodeRepository


def create_episode_repository(
    session: Session,
) -> EpisodeRepository:
    return EpisodeRepository(session)