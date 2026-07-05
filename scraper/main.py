import argparse

from scraper.core.http_client import HttpClient
from scraper.services.scraper_pipeline import ScraperPipeline
from scraper.services.scraper_services import ScraperServices
from scraper.utils.config_loader import load_provider_config

from scraper.database.session import SessionLocal

from scraper.crawlers.fandom_episode_index import FandomEpisodeIndexCrawler
from scraper.crawlers.naruto_episode_index import NarutoEpisodeIndexCrawler

from time import perf_counter


def main():
    parser = argparse.ArgumentParser(
        description="AnimeMangaDB Scraper"
    )

    parser.add_argument(
        "--config",
        default="configs/fandom/one_piece.json",
        help="Path to provider configuration file",
    )

    parser.add_argument(
        "--full-crawl",
        action="store_true",
        help="Ignore max_episodes and crawl every discovered episode",
    )

    parser.add_argument(
        "--start-episode",
        type=int,
        help="Override the starting episode number",
    )

    parser.add_argument(
        "--end-episode",
        type=int,
        help="Override the ending episode number",
    )

    parser.add_argument(
        "--max-episodes",
        type=int,
        help="Override the maximum number of episodes to process",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview episodes without scraping or saving",
    )

    args = parser.parse_args()

    config_path = args.config

    config = load_provider_config(config_path)
    
    if args.full_crawl:
        config.scraper.full_crawl = True

    if args.start_episode is not None:
        config.scraper.start_episode = args.start_episode

    if args.end_episode is not None:
        config.scraper.end_episode = args.end_episode

    if args.max_episodes is not None:
        config.scraper.max_episodes = args.max_episodes

    print(f"Series: {config.series}")
    print(f"Config: {config_path}")

    start_time = perf_counter()

    client = HttpClient()

    session = SessionLocal()
    services = ScraperServices(
        config=config,
        session=session,
    )

    provider = services.provider
    extractor = services.extractor
    repo = services.repository
    crawler = services.crawler

    pipeline = ScraperPipeline(
        config=config,
        provider=provider,
        client=client,
        extractor=extractor,
        repo=repo,
    )

    episode_refs = crawler.get_episode_list()

    processed_count = 0
    with_chapters_count = 0
    without_chapters_count = 0
    failed_episodes = []

    if config.scraper.start_episode is not None:
        episode_refs = [
            ref
            for ref in episode_refs
            if ref.episode_number >= config.scraper.start_episode
        ]

    if config.scraper.end_episode is not None:
        episode_refs = [
            ref
            for ref in episode_refs
            if ref.episode_number <= config.scraper.end_episode
        ]

    if not config.scraper.full_crawl:
        episode_refs = episode_refs[
            :config.scraper.max_episodes
        ]

    if args.dry_run:
        print("Dry run mode enabled.")

        for episode_ref in episode_refs:
            print(
                f"Would scrape Episode "
                f"{episode_ref.episode_number}: {episode_ref.url}"
            )

        return

    total = len(episode_refs)

    print(f"Discovered {total} episodes")

    for index, episode_ref in enumerate(
        episode_refs,
        start=1,
    ):
        episode_number = episode_ref.episode_number
        episode_url = episode_ref.url
        print(
            f"[{index}/{total}] "
            f"Scraping Episode {episode_number}"
        )

        try:
            result = pipeline.scrape_episode(
                episode_number=episode_number,
                episode_url=episode_url,
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