from scraper.core.http_client import HttpClient
from scraper.extractors.fandom_extractor import FandomExtractor
from scraper.providers.fandom_provider import FandomProvider
from scraper.utils.config_loader import load_provider_config

from scraper.database.session import SessionLocal
from scraper.repositories.episode_repository import EpisodeRepository


def scrape_episode(
    config,
    provider,
    client,
    extractor,
    repo,
    episode_number: int,
):
    # 1. Build URL
    url = provider.build_episode_url(episode_number)

    # 2. Fetch HTML
    html = client.fetch(url)

    # 3. Parse episode
    episode_data = extractor.parse(
        html=html,
        episode_number=episode_number,
        source_url=url,
    )

    # 4. Get or create anime
    anime = repo.get_or_create_anime(
        title=config.series,
        provider="fandom",
        base_url=config.base_url,
    )

    # 5. Save episode
    saved_episode = repo.create_episode(
        anime=anime,
        data=episode_data,
    )

    # 6. Save chapter mappings
    chapter_numbers = []

    if episode_data.manga_start is not None:
        if episode_data.manga_end is None:
            chapter_numbers = [episode_data.manga_start]
        else:
            chapter_numbers = list(
                range(
                    episode_data.manga_start,
                    episode_data.manga_end + 1,
                )
            )

    repo.add_episode_chapters(
        episode=saved_episode,
        chapter_numbers=chapter_numbers,
    )

    # 7. Output
    print(f"Episode ID: {saved_episode.id}")
    print(f"Title: {saved_episode.episode_title}")
    print(
        f"Chapters: "
        f"{episode_data.manga_start} → {episode_data.manga_end}"
    )


def main():
    # Load configuration
    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    # Initialize components
    provider = FandomProvider(config)
    client = HttpClient()
    extractor = FandomExtractor(config)

    session = SessionLocal()
    repo = EpisodeRepository(session)

    # Get episode list
    episodes = provider.get_episode_list()

    # Scrape all episodes
    for episode_number, _ in episodes:
        scrape_episode(
            config=config,
            provider=provider,
            client=client,
            extractor=extractor,
            repo=repo,
            episode_number=episode_number,
        )


if __name__ == "__main__":
    main()