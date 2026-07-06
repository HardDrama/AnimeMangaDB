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

            missing_arcs = [
                episode
                for episode in episodes
                if episode.arc is None
            ]

            episode_count = len(episodes)

            missing_chapter_percent = (
                len(missing_chapters) / episode_count * 100
                if episode_count
                else 0
            )

            generic_title_percent = (
                len(generic_titles) / episode_count * 100
                if episode_count
                else 0
            )

            missing_arc_percent = (
                len(missing_arcs) / episode_count * 100
                if episode_count
                else 0
            )

            print()
            print(f"Anime: {anime.title}")
            print(f"Episodes: {episode_count}")
            print(
                f"Missing chapter mappings: "
                f"{len(missing_chapters)} ({missing_chapter_percent:.1f}%)"
            )
            print(
                f"Generic episode titles: "
                f"{len(generic_titles)} ({generic_title_percent:.1f}%)"
            )
            print(
                f"Missing arcs: "
                f"{len(missing_arcs)} ({missing_arc_percent:.1f}%)"
            )

            if missing_chapter_percent > 25:
                print("WARNING: High missing chapter mapping rate")

            if generic_title_percent > 25:
                print("WARNING: High generic title rate")

            if missing_arc_percent > 25:
                print("WARNING: High missing arc rate")

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

            if missing_arcs:
                print("Sample missing arcs:")

                for episode in missing_arcs[:5]:
                    print(
                        f"- Episode {episode.episode_number}: "
                        f"{episode.episode_title}"
                    )

    finally:
        session.close()


if __name__ == "__main__":
    main()