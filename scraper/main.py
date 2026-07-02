from scraper.core.http_client import HttpClient
from scraper.extractors.fandom_extractor import FandomExtractor
from scraper.providers.fandom_provider import FandomProvider
from scraper.utils.config_loader import load_provider_config

from scraper.database.session import SessionLocal
from scraper.repositories.episode_repository import EpisodeRepository

from scraper.crawlers.fandom_episode_index import FandomEpisodeIndexCrawler


def scrape_episode(
    config,
    provider,
    client,
    extractor,
    repo,
    episode_number: int,
):
    url = provider.build_episode_url(episode_number)

    html = client.fetch(url)

    episode_data = extractor.parse(
        html=html,
        episode_number=episode_number,
        source_url=url,
    )

    anime = repo.get_or_create_anime(
        title=config.series,
        provider="fandom",
        base_url=config.base_url,
    )

    saved_episode = repo.create_episode(
        anime=anime,
        data=episode_data,
    )

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

    if episode_data.manga_start is None:
        chapter_display = "No chapter mapping found"
    else:
        chapter_display = (
            f"{episode_data.manga_start} → {episode_data.manga_end}"
        )

    print(f"Episode ID: {saved_episode.id}")
    print(f"Title: {saved_episode.episode_title}")
    print(f"Chapters: {chapter_display}")


def main():
    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    provider = FandomProvider(config)
    client = HttpClient()
    extractor = FandomExtractor(config)

    session = SessionLocal()
    repo = EpisodeRepository(session)

    crawler = FandomEpisodeIndexCrawler(config.base_url)
    episode_numbers = crawler.get_episode_list()

    # Limit crawl size during development.
    # Configure this in configs/fandom/one_piece.json.
    # Filter by episode range (optional)
    if config.scraper.start_episode is not None:
        episode_numbers = [
            episode
            for episode in episode_numbers
            if episode >= config.scraper.start_episode
        ]

    if config.scraper.end_episode is not None:
        episode_numbers = [
            episode
            for episode in episode_numbers
            if episode <= config.scraper.end_episode
        ]

    # Apply development limit unless performing a full crawl
    if not config.scraper.full_crawl:
        episode_numbers = episode_numbers[
            :config.scraper.max_episodes
        ]

    print(f"Discovered {len(episode_numbers)} episodes")

    total = len(episode_numbers)

    for index, episode_number in enumerate(
        episode_numbers,
        start=1,
    ):
        print(f"[{index}/{total}] Scraping Episode {episode_number}")

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