from scraper.core.http_client import HttpClient
from scraper.extractors.fandom_extractor import FandomExtractor
from scraper.providers.fandom_provider import FandomProvider
from scraper.utils.config_loader import load_provider_config

from scraper.database.session import SessionLocal
from scraper.repositories.episode_repository import EpisodeRepository


def main():
    # 1. Load provider config
    config = load_provider_config("configs/fandom/one_piece.json")

    # 2. Initialize core components
    provider = FandomProvider(config)
    client = HttpClient()
    extractor = FandomExtractor(config)

    # 3. Build URL and fetch HTML
    episode_number = 1130
    url = provider.build_episode_url(episode_number)
    html = client.fetch(url)

    # 4. Extract structured data
    episode_data = extractor.parse(
        html=html,
        episode_number=episode_number,
        source_url=url,
    )

    # 5. Database session + repository
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

    # 6. Optional: store chapters (if implemented)
    repo.add_episode_chapters(
        episode=saved_episode,
        chapter_numbers=episode_data.manga_start and [episode_data.manga_start] or [],
    )

    # 7. Output (clean)
    print(f"Episode ID: {saved_episode.id}")
    print(f"Title: {saved_episode.episode_title}")
    print(f"Chapters: {episode_data.manga_start} → {episode_data.manga_end}")


if __name__ == "__main__":
    main()