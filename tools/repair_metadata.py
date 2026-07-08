import argparse

from time import perf_counter

from scraper.database.models import Episode
from scraper.database.session import SessionLocal
from scraper.services.episode_metadata_service import (
    EpisodeMetadataService,
)
from scraper.services.metadata_repair_service import (
    MetadataRepairService,
)
from scraper.services.metadata_repair_application_service import (
    MetadataRepairApplicationService,
)


def format_elapsed_time(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60

    if minutes:
        return (
            f"{minutes}m "
            f"{remaining_seconds:.2f}s"
        )

    return f"{remaining_seconds:.2f}s"

def main():
    parser = argparse.ArgumentParser(
        description="Preview proposed metadata repairs."
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=1,
        help="Maximum episodes to preview.",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Preview or repair all episodes.",
    )

    parser.add_argument(
        "--episode",
        type=int,
        default=None,
        help="Specific episode number to repair.",
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply repairs instead of previewing them.",
    )

    parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirm that repairs should be applied.",
    )

    args = parser.parse_args()

    started_at = perf_counter()

    session = SessionLocal()

    try:
        query = (
            session.query(Episode)
            .order_by(Episode.id)
        )

        if args.episode is not None:
            query = query.filter(
                Episode.episode_number == args.episode
            )
        elif not args.all:
            query = query.limit(args.limit)

        episodes = query.all()

        if not episodes:
            print("No episodes found.")
            return

        metadata_service = EpisodeMetadataService()
        repair_service = MetadataRepairService()
        application_service = (
            MetadataRepairApplicationService()
        )

        if args.apply:
            print("Metadata Repair Tool")
            print("--------------------")
            print("Running in APPLY mode.")
            print("Database writes are ENABLED.")
            print()

            if not args.yes:
                print("Missing confirmation flag: --yes")
                print("No database changes will be made.")
                return

            print("Apply mode placeholder.")
            print("Repair plans will be passed to the application service.")
            print()
        else:
            print("Metadata Repair Tool")
            print("--------------------")
            print("Running in PREVIEW mode.")
            print("Database writes are disabled.")
            print()

        if args.all:
            print("Batch Mode: ALL episodes selected.")
            print("This may take a long time.")
            print()

        episodes_with_repairs = 0
        episodes_without_repairs = 0
        total_repairs = 0

        for index, episode in enumerate(
            episodes,
            start=1,
        ):
            
            print(
                f"[{index}/{len(episodes)}] "
                f"Episode {episode.episode_number}"
            )

            metadata = metadata_service.get_metadata(episode)

            plan = repair_service.build_repair_plan(
                episode,
                metadata,
            )

            if args.apply:
                result = application_service.apply(
                    episode,
                    plan,
                    session=session,
                    commit=args.apply and args.yes,
                )

                print(
                    f"Application Result: "
                    f"{result.applied} applied, "
                    f"{result.skipped} skipped."
                )
                if result.committed:
                    print("Database Updated : YES")
                else:
                    print("Database Updated : NO (Dry Run)")
                print()

                continue

            print()
            print(f"Episode {episode.episode_number}")
            print("-" * 20)

            if not plan.has_repairs:
                episodes_without_repairs += 1
                print("No repairs needed.")
                continue

            print(f"{len(plan.repairs)} repair(s) proposed.")
            episodes_with_repairs += 1
            total_repairs += len(plan.repairs)
            print()

            for repair in plan.repairs:
                print(repair.field.replace("_", " ").title())
                print(f"  Current : {repair.current_value}")
                print(f"  New     : {repair.new_value}")
                print()

        elapsed_seconds = perf_counter() - started_at

        print()
        print("Summary")
        print("-------")
        print(f"Episodes Checked         : {len(episodes)}")
        print(f"Episodes With Repairs    : {episodes_with_repairs}")
        print(f"Episodes Without Repairs : {episodes_without_repairs}")
        print(f"Total Repairs            : {total_repairs}")
        print(
            f"Elapsed Time             : "
            f"{format_elapsed_time(elapsed_seconds)}"
        )

    finally:
        session.close()


if __name__ == "__main__":
    main()