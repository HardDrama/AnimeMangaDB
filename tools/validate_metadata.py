from scraper.database.session import SessionLocal
from scraper.repositories.factory import create_episode_repository


def main():
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        anime_list = repo.list_anime()

        print("Metadata Validation Report")
        print("--------------------------")

        issue_count = 0

        for anime in anime_list:
            episodes = repo.list_episodes_for_anime(anime.id)

            if not anime.provider:
                issue_count += 1
                print(
                    f"[Missing Provider] {anime.title}"
                )

            if not anime.base_url:
                issue_count += 1
                print(
                    f"[Missing Base URL] {anime.title}"
                )
            
            for episode in episodes:
                if not episode.episode_title:
                    issue_count += 1
                    print(
                        f"[Missing Title] {anime.title} "
                        f"Episode {episode.episode_number}"
                    )

                if episode.episode_number <= 0:
                    issue_count += 1
                    print(
                        f"[Invalid Episode Number] {anime.title} "
                        f"Episode ID {episode.id}"
                    )

                if not episode.source_url:
                    issue_count += 1
                    print(
                        f"[Missing Source URL] {anime.title} "
                        f"Episode {episode.episode_number}"
                    )

                chapters = repo.get_chapters_for_episode_id(
                    episode.id
                )

                chapter_numbers = [
                    chapter.chapter_number
                    for chapter in chapters
                ]

                if len(chapter_numbers) != len(set(chapter_numbers)):
                    issue_count += 1
                    print(
                        f"[Duplicate Chapters] {anime.title} "
                        f"Episode {episode.episode_number}"
                    )

                if chapter_numbers != sorted(chapter_numbers):
                    issue_count += 1
                    print(
                        f"[Unsorted Chapters] {anime.title} "
                        f"Episode {episode.episode_number}"
                    )

        print()
        print(f"Total issues found: {issue_count}")

    finally:
        session.close()


if __name__ == "__main__":
    main()