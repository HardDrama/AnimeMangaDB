from scraper.database.session import SessionLocal
from scraper.repositories.factory import create_episode_repository


def main():
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        anime_list = repo.list_anime()

        print("AnimeMangaDB Data Quality Report")
        print("--------------------------------")

        for anime in anime_list:
            episodes = repo.list_episodes_for_anime(anime.id)

            missing_chapters = [
                episode
                for episode in episodes
                if not repo.get_chapters_for_episode_id(episode.id)
            ]

            generic_titles = [
                episode
                for episode in episodes
                if episode.episode_title
                == f"Episode {episode.episode_number}"
            ]

            print()
            print(f"Anime: {anime.title}")
            print(f"Episodes: {len(episodes)}")
            print(f"Missing chapter mappings: {len(missing_chapters)}")
            print(f"Generic episode titles: {len(generic_titles)}")

            if missing_chapters:
                print("Sample missing chapter mappings:")

                for episode in missing_chapters[:5]:
                    print(
                        f"- Episode {episode.episode_number}: "
                        f"{episode.episode_title}"
                    )

            if generic_titles:
                print("Sample generic episode titles:")

                for episode in generic_titles[:5]:
                    print(
                        f"- Episode {episode.episode_number}: "
                        f"{episode.episode_title}"
                    )

    finally:
        session.close()


if __name__ == "__main__":
    main()