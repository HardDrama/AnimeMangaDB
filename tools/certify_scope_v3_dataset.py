import argparse
import json
from datetime import datetime
from pathlib import Path


def load_json_file(
    path: str,
) -> dict:
    report_path = Path(path)

    if not report_path.exists():
        raise ValueError(
            f"Report file not found: {report_path}"
        )

    try:
        return json.loads(
            report_path.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON report: {report_path}"
        ) from error


def validate_audit_report(
    report: dict,
    anime_title: str,
    expected_start: int,
    expected_end: int,
) -> list[str]:
    failures = []

    if report.get("anime") != anime_title:
        failures.append(
            "Audit report anime does not match."
        )

    if (
        report.get("expected_start_chapter")
        != expected_start
    ):
        failures.append(
            "Audit report start chapter does not match."
        )

    if (
        report.get("expected_end_chapter")
        != expected_end
    ):
        failures.append(
            "Audit report end chapter does not match."
        )

    if (
        report.get("metadata_audit_status")
        != "PASS"
    ):
        failures.append(
            "Metadata audit status is not PASS."
        )

    if (
        report.get("coverage_audit_status")
        != "PASS"
    ):
        failures.append(
            "Coverage audit status is not PASS."
        )

    if report.get("dataset_status") != "PASS":
        failures.append(
            "Dataset audit status is not PASS."
        )

    if report.get("missing_chapters") != 0:
        failures.append(
            "Audit report contains missing chapters."
        )

    if report.get("duplicate_chapters") != 0:
        failures.append(
            "Audit report contains duplicate chapters."
        )

    if report.get("missing_titles") != 0:
        failures.append(
            "Audit report contains missing titles."
        )

    if report.get("unresolved_missing_arcs", 0) != 0:
        failures.append(
            "Audit report contains unresolved manga arcs."
        )

    if report.get(
        "configured_missing_arc_records",
        [],
    ):
        failures.append(
            "Audit report contains invalid manga arc exceptions."
        )

    if report.get("missing_source_urls") != 0:
        failures.append(
            "Audit report contains missing source URLs."
        )

    if report.get("missing_last_updated") != 0:
        failures.append(
            "Audit report contains missing timestamps."
        )

    return failures


def validate_manual_report(
    report: dict,
    anime_title: str,
) -> list[str]:
    failures = []

    if report.get("anime") != anime_title:
        failures.append(
            "Manual report anime does not match."
        )

    if (
        report.get("validation_status")
        != "PASS"
    ):
        failures.append(
            "Manual validation status is not PASS."
        )

    results = report.get(
        "results",
        []
    )

    if not results:
        failures.append(
            "Manual validation contains no samples."
        )

        return failures

    for result in results:
        chapter_number = result.get(
            "chapter_number"
        )

        if not result.get(
            "record_found",
            False,
        ):
            failures.append(
                f"Chapter {chapter_number} record "
                "was not found."
            )

        if (
            result.get("manual_title_match")
            is not True
        ):
            failures.append(
                f"Chapter {chapter_number} title "
                "was not validated."
            )

        if (
            result.get("manual_arc_match")
            is not True
        ):
            failures.append(
                f"Chapter {chapter_number} manga arc "
                "was not validated."
            )

        if (
            result.get("manual_url_valid")
            is not True
        ):
            failures.append(
                f"Chapter {chapter_number} source URL "
                "was not validated."
            )

    return failures


def build_certification_report(
    anime_title: str,
    expected_start: int,
    expected_end: int,
    audit_report: dict,
    manual_report: dict,
) -> dict:
    audit_failures = validate_audit_report(
        report=audit_report,
        anime_title=anime_title,
        expected_start=expected_start,
        expected_end=expected_end,
    )

    manual_failures = validate_manual_report(
        report=manual_report,
        anime_title=anime_title,
    )

    failures = (
        audit_failures
        + manual_failures
    )

    certification_eligible = (
        len(failures) == 0
    )

    return {
        "schema_version": 1,
        "anime": anime_title,
        "expected_start_chapter": (
            expected_start
        ),
        "expected_end_chapter": (
            expected_end
        ),
        "expected_chapter_count": (
            expected_end
            - expected_start
            + 1
        ),
        "metadata_audit_status": (
            audit_report.get(
                "metadata_audit_status"
            )
        ),
        "coverage_audit_status": (
            audit_report.get(
                "coverage_audit_status"
            )
        ),
        "dataset_audit_status": (
            audit_report.get(
                "dataset_status"
            )
        ),
        "manual_validation_status": (
            manual_report.get(
                "validation_status"
            )
        ),
        "manual_samples_reviewed": len(
            manual_report.get(
                "results",
                [],
            )
        ),
        "failure_count": len(
            failures
        ),
        "failures": failures,
        "certification_eligible": (
            certification_eligible
        ),
        "certification_status": (
            "ELIGIBLE"
            if certification_eligible
            else "NOT ELIGIBLE"
        ),
        "generated_at": (
            datetime.now().isoformat()
        ),
    }


def print_certification_report(
    report: dict,
) -> None:
    print("Scope v3 Dataset Certification Audit")
    print("------------------------------------")
    print(f"Anime                  : {report['anime']}")
    print(
        f"Expected Range         : "
        f"{report['expected_start_chapter']}"
        f"–{report['expected_end_chapter']}"
    )
    print(
        f"Expected Chapters      : "
        f"{report['expected_chapter_count']}"
    )
    print()
    print(
        f"Metadata Audit         : "
        f"{report['metadata_audit_status']}"
    )
    print(
        f"Coverage Audit         : "
        f"{report['coverage_audit_status']}"
    )
    print(
        f"Dataset Audit          : "
        f"{report['dataset_audit_status']}"
    )
    print(
        f"Manual Validation      : "
        f"{report['manual_validation_status']}"
    )
    print(
        f"Manual Samples         : "
        f"{report['manual_samples_reviewed']}"
    )
    print()
    print(
        f"Certification Status   : "
        f"{report['certification_status']}"
    )

    if report["failures"]:
        print()
        print("Certification Failures")
        print("----------------------")

        for failure in report["failures"]:
            print(f"- {failure}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate Scope v3 dataset evidence "
            "for certification eligibility."
        )
    )

    parser.add_argument(
        "--anime",
        required=True,
        help="Anime dataset to evaluate.",
    )

    parser.add_argument(
        "--expected-start",
        type=int,
        required=True,
        help="First expected chapter.",
    )

    parser.add_argument(
        "--expected-end",
        type=int,
        required=True,
        help="Last expected chapter.",
    )

    parser.add_argument(
        "--audit-report",
        required=True,
        help=(
            "Path to the Scope v3 audit JSON report."
        ),
    )

    parser.add_argument(
        "--manual-report",
        required=True,
        help=(
            "Path to the manual validation JSON report."
        ),
    )

    parser.add_argument(
        "--json-report",
        default=None,
        help=(
            "Write the certification eligibility "
            "report to a JSON file."
        ),
    )

    args = parser.parse_args()

    if args.expected_start > args.expected_end:
        print(
            "Expected start chapter must be less "
            "than or equal to expected end chapter."
        )
        return

    try:
        audit_report = load_json_file(
            args.audit_report
        )

        manual_report = load_json_file(
            args.manual_report
        )

    except ValueError as error:
        print(error)
        return

    report = build_certification_report(
        anime_title=args.anime,
        expected_start=args.expected_start,
        expected_end=args.expected_end,
        audit_report=audit_report,
        manual_report=manual_report,
    )

    print_certification_report(
        report
    )

    if args.json_report:
        report_path = Path(
            args.json_report
        )

        report_path.write_text(
            json.dumps(
                report,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        print()
        print(
            "Certification report written to: "
            f"{report_path}"
        )


if __name__ == "__main__":
    main()