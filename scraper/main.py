from scraper.core.http_client import HttpClient
from scraper.extractors.fandom_extractor import FandomExtractor
from scraper.providers.fandom_provider import FandomProvider
from scraper.utils.config_loader import load_provider_config

from scraper.database.session import SessionLocal
from scraper.repositories.episode_repository import EpisodeRepository

from scraper.crawlers.fandom_episode_index import FandomEpisodeIndexCrawler

from time import perf_counter


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

    if repo.chapter_mappings_need_update(
        episode=saved_episode,
        chapter_numbers=chapter_numbers,
    ):
        repo.replace_episode_chapters(
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

    return {
        "episode_number": episode_number,
        "has_chapters": episode_data.manga_start is not None,
    }


def main():
    config_path = "configs/fandom/one_piece.json"

    config = load_provider_config(config_path)

    print(f"Series: {config.series}")
    print(f"Config: {config_path}")

    start_time = perf_counter()

    provider = FandomProvider(config)
    client = HttpClient()
    extractor = FandomExtractor(config)

    session = SessionLocal()
    repo = EpisodeRepository(session)

    crawler = FandomEpisodeIndexCrawler(config.base_url)
    episode_numbers = crawler.get_episode_list()

    processed_count = 0
    with_chapters_count = 0
    without_chapters_count = 0
    failed_episodes = []

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

    if not config.scraper.full_crawl:
        episode_numbers = episode_numbers[
            :config.scraper.max_episodes
        ]

    total = len(episode_numbers)

    print(f"Discovered {total} episodes")

    for index, episode_number in enumerate(
        episode_numbers,
        start=1,
    ):
        print(
            f"[{index}/{total}] "
            f"Scraping Episode {episode_number}"
        )

        try:
            result = scrape_episode(
                config=config,
                provider=provider,
                client=client,
                extractor=extractor,
                repo=repo,
                episode_number=episode_number,
            )

            processed_count += 1

            if result["has_chapters"]:
                with_chapters_count += 1
            else:
                without_chapters_count += 1

        except Exception as error:
            failed_episodes.append(
                {
                    "episode_number": episode_number,
                    "error": str(error),
                }
            )

            print(f"FAILED Episode {episode_number}: {error}")

    elapsed = perf_counter() - start_time

    print("\nCrawl summary")
    print("-------------")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    print(f"Episodes processed: {processed_count}")
    print(f"Episodes with chapters: {with_chapters_count}")
    print(f"Episodes without chapters: {without_chapters_count}")
    print(f"Episodes failed: {len(failed_episodes)}")

    if failed_episodes:
        print("Failed episodes:")
        for failed in failed_episodes:
            print(
                f"- Episode {failed['episode_number']}: "
                f"{failed['error']}"
            )


if __name__ == "__main__":
    main()