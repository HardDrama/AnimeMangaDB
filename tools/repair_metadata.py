import argparse

import json
from pathlib import Path

import csv

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

    parser.add_argument(
        "--csv-report",
        type=str,
        default=None,
        help="Write repair episode results to a CSV file.",
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
            "episode_totals": {},
            "failure_details": {},
            "report_path": None,
            "report_format": "json",
            "episodes": [],
            "status_totals": {},
            "field_totals": {},
        }

        if args.csv_report:
            with open(
                args.csv_report,
                "w",
                newline="",
                encoding="utf-8",
            ) as csv_file:
                writer = csv.DictWriter(
                    csv_file,
                    fieldnames=[
                        "episode_id",
                        "anime_title",
                        "provider",
                        "episode_number",
                        "source_url",
                        "current_title",
                        "current_arc",
                        "status",
                        "repairs_proposed",
                        "repairs_applied",
                        "repairs_skipped",
                        "fields",
                        "repair_details",
                    ],
                )

                writer.writeheader()

                for episode_result in report["episodes"]:
                    writer.writerow(
                        {
                            "episode_id": episode_result.get("episode_id"),
                            "anime_title": episode_result.get("anime_title"),
                            "provider": episode_result.get("provider"),
                            "episode_number": episode_result.get("episode_number"),
                            "source_url": episode_result.get("source_url"),
                            "current_title": episode_result.get("current_title"),
                            "current_arc": episode_result.get("current_arc"),
                            "status": episode_result.get("status"),
                            "repairs_proposed": episode_result.get(
                                "repairs_proposed",
                                0,
                            ),
                            "repairs_applied": episode_result.get(
                                "repairs_applied",
                                0,
                            ),
                            "repairs_skipped": episode_result.get(
                                "repairs_skipped",
                                0,
                            ),
                            "fields": ",".join(
                                episode_result.get("fields", [])
                            ),
                            "repair_details": "; ".join(
                                (
                                    f"{repair.get('field')}: "
                                    f"{repair.get('current_value')} -> "
                                    f"{repair.get('new_value')}"
                                )
                                for repair in episode_result.get("repairs", [])
                            ),
                        }
                    )

                writer.writerow({})

                writer.writerow(
                    {
                        "episode_number": "SUMMARY",
                        "status": report["status"],
                        "repairs_proposed": total_repairs,
                        "repairs_applied": total_applied_repairs,
                        "repairs_skipped": total_skipped_repairs,
                    }
                )

                writer.writerow(
                    {
                        "episode_number": "REPORT_FORMAT",
                        "status": "csv",
                        "repairs_proposed": "schema_version",
                        "repairs_applied": 1,
                    }
                )

                writer.writerow(
                    {
                        "episode_number": "GENERATED_AT",
                        "status": datetime.now().isoformat(),
                    }
                )

                writer.writerow({})

                writer.writerow(
                    {
                        "episode_number": "EPISODES",
                        "status": len(episodes),
                        "repairs_proposed": episodes_updated,
                        "repairs_applied": episodes_with_repairs,
                        "repairs_skipped": episodes_without_repairs,
                    }
                )

            print()
            print(f"CSV report written to: {args.csv_report}")

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

                    report["episodes"].append(
                        {
                            "anime_title": episode.anime.title,
                            "provider": episode.anime.provider,
                            "episode_id": episode.id,
                            "episode_number": episode.episode_number,
                            "source_url": episode.source_url,
                            "current_title": episode.episode_title,
                            "current_arc": episode.arc,
                            "repairs_proposed": len(plan.repairs),
                            "repairs_applied": result.applied,
                            "repairs_skipped": result.skipped,
                            "fields": [
                                repair.field
                                for repair in plan.repairs
                            ],
                            "repairs": [
                                {
                                    "field": repair.field,
                                    "current_value": repair.current_value,
                                    "new_value": repair.new_value,
                                }
                                for repair in plan.repairs
                            ],
                            "status": (
                                "updated"
                                if result.applied > 0
                                else "up_to_date"
                            ),
                        }
                    )

                    continue

                if not plan.has_repairs:
                    episodes_without_repairs += 1
                    print("No repairs needed.")

                    report["episodes"].append(
                        {
                            "anime_title": episode.anime.title,
                            "provider": episode.anime.provider,
                            "episode_id": episode.id,
                            "episode_number": episode.episode_number,
                            "source_url": episode.source_url,
                            "current_title": episode.episode_title,
                            "current_arc": episode.arc,
                            "repairs_proposed": 0,
                            "repairs_applied": 0,
                            "repairs_skipped": 0,
                            "fields": [],
                            "repairs": [],
                            "status": "up_to_date",
                        }
                    )

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

                report["episodes"].append(
                    {
                        "anime_title": episode.anime.title,
                        "provider": episode.anime.provider,
                        "episode_id": episode.id,
                        "episode_number": episode.episode_number,
                        "source_url": episode.source_url,
                        "current_title": episode.episode_title,
                        "current_arc": episode.arc,
                        "repairs_proposed": len(plan.repairs),
                        "repairs_applied": 0,
                        "repairs_skipped": 0,
                        "fields": [
                            repair.field
                            for repair in plan.repairs
                        ],
                        "repairs": [
                            {
                                "field": repair.field,
                                "current_value": repair.current_value,
                                "new_value": repair.new_value,
                            }
                            for repair in plan.repairs
                        ],
                        "status": "needs_repairs",
                    }
                )

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

                report["episodes"].append(
                    {
                        "anime_title": episode.anime.title,
                        "provider": episode.anime.provider,
                        "episode_id": episode.id,
                        "episode_number": episode.episode_number,
                        "source_url": episode.source_url,
                        "current_title": episode.episode_title,
                        "current_arc": episode.arc,
                        "fields": [],
                        "repairs": [],
                        "status": "failed",
                        "error": str(exc),
                    }
                )

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

        status_totals = {}

        for episode_result in report["episodes"]:
            status = episode_result["status"]

            status_totals[status] = (
                status_totals.get(status, 0) + 1
            )

        field_totals = {}

        for episode_result in report["episodes"]:
            for field in episode_result["fields"]:
                field_totals[field] = (
                    field_totals.get(field, 0) + 1
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
                "episode_totals": {
                    "checked": len(episodes),
                    "updated": episodes_updated,
                    "with_repairs": episodes_with_repairs,
                    "without_repairs": episodes_without_repairs,
                    "failed": failed_episodes,
                },
                "failure_details": {
                    "count": failed_episodes,
                    "episode_numbers": failed_episode_numbers,
                    "reasons": [
                        {
                            "episode_number": episode_number,
                            "reason": reason,
                        }
                        for episode_number, reason in failure_reasons
                    ],
                },
                "report_path": args.json_report,
                "status_totals": status_totals,
                "field_totals": field_totals,
            }
        )

        if args.json_report:
            Path(args.json_report).write_text(
                json.dumps(report, indent=2),
                encoding="utf-8",
            )

            print()
            print(f"JSON report written to: {args.json_report}")

        written_reports = []

        if args.json_report:
            written_reports.append(args.json_report)

        if args.csv_report:
            written_reports.append(args.csv_report)

        if written_reports:
            print()
            print("Reports Written")
            print("---------------")

            for report_path in written_reports:
                print(f"- {report_path}")

    finally:
        session.close()


if __name__ == "__main__":
    main()