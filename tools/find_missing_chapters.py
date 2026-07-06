from scraper.database.session import SessionLocal
from scraper.repositories.factory import create_episode_repository


def main():
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        anime_list = repo.list_anime()

        print("Missing Chapter Mapping Report")
        print("------------------------------")

        for anime in anime_list:
            episodes = repo.list_episodes_for_anime(anime.id)

            missing_chapters = [
                episode
                for episode in episodes
                if not repo.get_chapters_for_episode_id(episode.id)
            ]

            print()
            print(f"Anime: {anime.title}")
            print(f"Missing chapter mappings: {len(missing_chapters)}")

            for episode in missing_chapters[:10]:
                print(
                    f"- Episode {episode.episode_number}: "
                    f"{episode.episode_title}"
                )

    finally:
        session.close()


if __name__ == "__main__":
    main()