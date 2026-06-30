from scraper.core.http_client import HttpClient
from scraper.extractors.fandom_extractor import FandomExtractor
from scraper.providers.fandom_provider import FandomProvider
from scraper.utils.config_loader import load_provider_config

from scraper.database.session import SessionLocal
from scraper.repositories.episode_repository import EpisodeRepository


def main():
    config = load_provider_config("configs/fandom/one_piece.json")

    provider = FandomProvider(config)
    client = HttpClient()
    extractor = FandomExtractor(config)

    url = provider.build_episode_url(1130)
    html = client.fetch(url)

    episode_data = extractor.parse(
        html=html,
        episode_number=1130,
        source_url=url,
    )

    session = SessionLocal()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title=config.series,
        provider="fandom",
        base_url=config.base_url,
    )

    saved_episode = repo.create_episode(
        anime=anime,
        data=episode_data,
    )

    print("CHAPTER NUMBERS:", episode_data.chapter_numbers)

    repo.add_episode_chapters(
        episode=saved_episode,
        chapter_numbers=episode_data.chapter_numbers,
    )

    print("Episode ID:", saved_episode.id)
    print("Title:", saved_episode.episode_title)


if __name__ == "__main__":
    main()