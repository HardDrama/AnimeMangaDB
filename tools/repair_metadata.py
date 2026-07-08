import argparse

import json
from pathlib import Path

from time import perf_counter

from datetime import datetime

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

    parser.add_argument(
        "--json-report",
        type=str,
        default=None,
        help="Write repair summary report to a JSON file.",
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
        failed_episodes = 0
        failed_episode_numbers = []
        failure_reasons = []
        total_applied_repairs = 0
        total_skipped_repairs = 0
        total_repairs = 0
        episodes_updated = 0
        report = {
            "schema_version": 1,
            "episodes_checked": 0,
            "episodes_updated": 0,
            "episodes_with_repairs": 0,
            "episodes_without_repairs": 0,
            "failed_episodes": 0,
            "failed_episode_numbers": [],
            "failure_reasons": [],
            "applied_repairs": 0,
            "skipped_repairs": 0,
            "generated_at": None,
            "mode": None,
            "selection": None,
            "elapsed_seconds": 0,
            "status": None,
            "arguments": {},
            "is_apply_mode": False,
            "is_preview_mode": False,
            "is_all_episodes": False,
            "is_single_episode": False,
            "repair_totals": {},
        }

        for index, episode in enumerate(
            episodes,
            start=1,
        ):
            print(
                f"[{index}/{len(episodes)}] "
                f"Episode {episode.episode_number}"
            )

            try:
                metadata = metadata_service.get_metadata(
                    episode
                )

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

                    total_applied_repairs += result.applied
                    total_skipped_repairs += result.skipped

                    if result.applied > 0:
                        episodes_updated += 1

                    if plan.has_repairs:
                        episodes_with_repairs += 1
                        total_repairs += len(plan.repairs)
                    else:
                        episodes_without_repairs += 1

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

                if not plan.has_repairs:
                    episodes_without_repairs += 1
                    print("No repairs needed.")
                    continue

                episodes_with_repairs += 1
                total_repairs += len(plan.repairs)

                print(f"{len(plan.repairs)} repair(s) proposed.")
                print()

                for repair in plan.repairs:
                    print(repair.field.replace("_", " ").title())
                    print(f"  Current : {repair.current_value}")
                    print(f"  New     : {repair.new_value}")
                    print()

            except Exception as exc:
                failed_episodes += 1
                failed_episode_numbers.append(
                    episode.episode_number
                )
                failure_reasons.append(
                    (
                        episode.episode_number,
                        str(exc),
                    )
                )
                print(f"FAILED: {exc}")
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
        print(f"Failed Episodes          : {failed_episodes}")
        if failed_episode_numbers:
            print(
                "Failed Episode Numbers   : "
                + ", ".join(
                    str(number)
                    for number in failed_episode_numbers
                )
            )
        if failure_reasons:
            print("Failure Reasons:")
            for episode_number, reason in failure_reasons:
                print(f"  Episode {episode_number}: {reason}")
        print(f"Applied Repairs          : {total_applied_repairs}")
        print(f"Skipped Repairs          : {total_skipped_repairs}")
        print(f"Total Repairs            : {total_repairs}")
        print(f"Episodes Updated         : {episodes_updated}")
        print(
            f"Elapsed Time             : "
            f"{format_elapsed_time(elapsed_seconds)}"
        )
        print()

        if failed_episodes:
            print("Status: Completed with failures.")
        else:
            print("Status: Completed successfully.")

        status = (
            "completed_with_failures"
            if failed_episodes
            else "completed_successfully"
        )
        
        report.update(
            {
                "episodes_checked": len(episodes),
                "episodes_updated": episodes_updated,
                "episodes_with_repairs": episodes_with_repairs,
                "episodes_without_repairs": episodes_without_repairs,
                "failed_episodes": failed_episodes,
                "failed_episode_numbers": failed_episode_numbers,
                "failure_reasons": failure_reasons,
                "applied_repairs": total_applied_repairs,
                "skipped_repairs": total_skipped_repairs,
                "generated_at": datetime.now().isoformat(),
                "mode": "apply" if args.apply else "preview",
                "selection": (
                    "all"
                    if args.all
                    else (
                        f"episode:{args.episode}"
                        if args.episode is not None
                        else f"limit:{args.limit}"
                    )
                ),
                "elapsed_seconds": round(elapsed_seconds, 2),
                "status": status,
                "arguments": {
                    "limit": args.limit,
                    "episode": args.episode,
                    "all": args.all,
                    "apply": args.apply,
                    "yes": args.yes,
                    "json_report": args.json_report,
                },
                "is_apply_mode": args.apply,
                "is_preview_mode": not args.apply,
                "is_all_episodes": args.all,
                "is_single_episode": args.episode is not None,
                "repair_totals": {
                    "proposed": total_repairs,
                    "applied": total_applied_repairs,
                    "skipped": total_skipped_repairs,
                },
            }
        )

        if args.json_report:
            Path(args.json_report).write_text(
                json.dumps(report, indent=2),
                encoding="utf-8",
            )

            print()
            print(f"JSON report written to: {args.json_report}")

    finally:
        session.close()


if __name__ == "__main__":
    main()