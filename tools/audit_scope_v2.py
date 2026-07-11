import argparse
import json
from pathlib import Path

from scraper.database.models import Anime, Episode
from scraper.database.session import SessionLocal
from scraper.utils.metadata_exception_loader import (
    get_arc_not_applicable_episodes,
    load_metadata_exceptions,
)


def main():
    parser = argparse.ArgumentParser(
        description="Audit Scope v2 database readiness."
    )

    parser.add_argument(
        "--json-report",
        type=str,
        default=None,
        help="Write Scope v2 audit results to a JSON file.",
    )

    parser.add_argument(
        "--anime",
        type=str,
        default="One Piece",
        help="Anime title to audit. Defaults to One Piece.",
    )

    args = parser.parse_args()

    session = SessionLocal()

    try:
        anime = (
            session.query(Anime)
            .filter(Anime.title == args.anime)
            .first()
        )

        if anime is None:
            print(
                f'Anime not found: "{args.anime}"'
            )
            return
        
        exception_path = (
            f"configs/exceptions/"
            f"{anime.title.lower().replace(' ', '_')}.json"
        )

        try:
            exceptions = load_metadata_exceptions(
                exception_path
            )
        except FileNotFoundError:
            exceptions = {}

        arc_not_applicable_numbers = (
            get_arc_not_applicable_episodes(
                exceptions
            )
        )

        episodes = (
            session.query(Episode)
            .filter(Episode.anime_id == anime.id)
            .order_by(Episode.episode_number)
            .all()
        )

        total = len(episodes)

        missing_titles = [
            episode
            for episode in episodes
            if not episode.episode_title
            or episode.episode_title
            == f"Episode {episode.episode_number}"
        ]

        empty_titles = [
            episode
            for episode in episodes
            if not episode.episode_title
        ]

        placeholder_titles = [
            episode
            for episode in episodes
            if episode.episode_title
            == f"Episode {episode.episode_number}"
        ]

        missing_arcs = [
            episode
            for episode in episodes
            if not episode.arc
        ]

        arc_not_applicable = [
            episode
            for episode in missing_arcs
            if episode.episode_number
            in arc_not_applicable_numbers
        ]

        unresolved_missing_arcs = [
            episode
            for episode in missing_arcs
            if episode.episode_number
            not in arc_not_applicable_numbers
        ]

        episodes_with_arcs = [
            episode
            for episode in episodes
            if episode.arc
        ]

        episodes_with_titles = total - len(missing_titles)

        arc_count = total - len(
            unresolved_missing_arcs
        )

        title_percent = (
            episodes_with_titles / total * 100
            if total
            else 0
        )

        arc_percent = (
            arc_count / total * 100
            if total
            else 0
        )

        if title_percent == 100 and arc_percent == 100:
            audit_status = "PASS"
        elif title_percent >= 95 and arc_percent >= 95:
            audit_status = "NEARLY COMPLETE"
        else:
            audit_status = "IN PROGRESS"

        print("Scope v2 Database Audit")
        print("-----------------------")
        print(f"Anime: {anime.title}")
        print()
        print(f"Episodes Checked : {total}")
        print(f"Missing Titles   : {len(missing_titles)}")
        print(f"Empty Titles     : {len(empty_titles)}")
        print(f"Placeholder Titles: {len(placeholder_titles)}")
        print(f"Title Completion : {title_percent:.2f}%")
        print(f"Raw Missing Arcs : {len(missing_arcs)}")
        print(
            f"Arc Not Applicable: "
            f"{len(arc_not_applicable)}"
        )
        print(
            f"Unresolved Arc Gaps: "
            f"{len(unresolved_missing_arcs)}"
        )
        print(
            f"Episodes With Arcs: "
            f"{len(episodes_with_arcs)}"
        )
        print(
            f"Effective Arc Completion: "
            f"{arc_percent:.2f}%"
        )
        print()
        print(f"Audit Status     : {audit_status}")

        if missing_titles:
            print()
            print("Episodes Missing Titles")
            print("-----------------------")
            for episode in missing_titles[:25]:
                print(f"Episode {episode.episode_number}")

        if arc_not_applicable:
            print()
            print("Episodes With Arc Not Applicable")
            print("--------------------------------")
            for episode in arc_not_applicable[:25]:
                print(f"Episode {episode.episode_number}")

        if unresolved_missing_arcs:
            print()
            print("Episodes With Unresolved Arc Gaps")
            print("---------------------------------")
            for episode in unresolved_missing_arcs[:25]:
                print(f"Episode {episode.episode_number}")

        if placeholder_titles:
            print()
            print("Episodes With Placeholder Titles")
            print("--------------------------------")
            for episode in placeholder_titles[:25]:
                print(f"Episode {episode.episode_number}")

        if args.json_report:
            report = {
                "anime": anime.title,
                "episodes_checked": total,
                "missing_titles": len(missing_titles),
                "empty_titles": len(empty_titles),
                "placeholder_titles": len(placeholder_titles),
                "missing_arcs": len(missing_arcs),
                "arc_not_applicable": len(
                    arc_not_applicable
                ),
                "unresolved_arc_gaps": len(
                    unresolved_missing_arcs
                ),
                "effective_arc_completion": round(
                    arc_percent,
                    2,
                ),
                "episodes_with_arcs": len(episodes_with_arcs),
                "title_completion": round(title_percent, 2),
                "arc_completion": round(arc_percent, 2),
                "audit_status": audit_status,
                "missing_title_episodes": [
                    episode.episode_number
                    for episode in missing_titles
                ],
                "empty_title_episodes": [
                    episode.episode_number
                    for episode in empty_titles
                ],
                "placeholder_title_episodes": [
                    episode.episode_number
                    for episode in placeholder_titles
                ],
                "missing_arc_episodes": [
                    episode.episode_number
                    for episode in missing_arcs
                ],
                "arc_not_applicable_episodes": [
                    episode.episode_number
                    for episode in arc_not_applicable
                ],
                "unresolved_arc_gap_episodes": [
                    episode.episode_number
                    for episode in unresolved_missing_arcs
                ],
            }

            Path(args.json_report).write_text(
                json.dumps(report, indent=2),
                encoding="utf-8",
            )

            print()
            print(f"Audit report written to: {args.json_report}")

    finally:
        session.close()


if __name__ == "__main__":
    main()