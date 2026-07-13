import json
import sys

import pytest

from tools import certify_scope_v3_dataset


def complete_audit_report() -> dict:
    return {
        "anime": "One Piece",
        "expected_start_chapter": 1,
        "expected_end_chapter": 1188,
        "metadata_audit_status": "PASS",
        "coverage_audit_status": "PASS",
        "dataset_status": "PASS",
        "missing_chapters": 0,
        "duplicate_chapters": 0,
        "missing_titles": 0,
        "missing_arcs": 0,
        "missing_source_urls": 0,
        "missing_last_updated": 0,
    }


def complete_manual_report() -> dict:
    return {
        "anime": "One Piece",
        "validation_status": "PASS",
        "results": [
            {
                "chapter_number": 1,
                "record_found": True,
                "manual_title_match": True,
                "manual_arc_match": True,
                "manual_url_valid": True,
            },
            {
                "chapter_number": 1188,
                "record_found": True,
                "manual_title_match": True,
                "manual_arc_match": True,
                "manual_url_valid": True,
            },
        ],
    }


def test_complete_evidence_is_eligible():
    report = (
        certify_scope_v3_dataset
        .build_certification_report(
            anime_title="One Piece",
            expected_start=1,
            expected_end=1188,
            audit_report=complete_audit_report(),
            manual_report=complete_manual_report(),
        )
    )

    assert report["failure_count"] == 0
    assert (
        report["certification_eligible"]
        is True
    )
    assert (
        report["certification_status"]
        == "ELIGIBLE"
    )


def test_failed_audit_is_not_eligible():
    audit_report = complete_audit_report()
    audit_report[
        "coverage_audit_status"
    ] = "IN PROGRESS"

    report = (
        certify_scope_v3_dataset
        .build_certification_report(
            anime_title="One Piece",
            expected_start=1,
            expected_end=1188,
            audit_report=audit_report,
            manual_report=complete_manual_report(),
        )
    )

    assert (
        report["certification_eligible"]
        is False
    )
    assert (
        report["certification_status"]
        == "NOT ELIGIBLE"
    )
    assert (
        "Coverage audit status is not PASS."
        in report["failures"]
    )


def test_failed_manual_sample_is_not_eligible():
    manual_report = complete_manual_report()

    manual_report["results"][0][
        "manual_arc_match"
    ] = False

    report = (
        certify_scope_v3_dataset
        .build_certification_report(
            anime_title="One Piece",
            expected_start=1,
            expected_end=1188,
            audit_report=complete_audit_report(),
            manual_report=manual_report,
        )
    )

    assert (
        report["certification_eligible"]
        is False
    )
    assert any(
        "Chapter 1 manga arc"
        in failure
        for failure in report["failures"]
    )


def test_missing_report_file_raises(
    tmp_path,
):
    missing_path = (
        tmp_path
        / "missing.json"
    )

    with pytest.raises(
        ValueError,
        match="Report file not found",
    ):
        certify_scope_v3_dataset.load_json_file(
            str(missing_path)
        )


def test_cli_writes_certification_report(
    monkeypatch,
    tmp_path,
):
    audit_path = (
        tmp_path
        / "audit.json"
    )

    manual_path = (
        tmp_path
        / "manual.json"
    )

    certification_path = (
        tmp_path
        / "certification.json"
    )

    audit_path.write_text(
        json.dumps(
            complete_audit_report()
        ),
        encoding="utf-8",
    )

    manual_path.write_text(
        json.dumps(
            complete_manual_report()
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "certify_scope_v3_dataset",
            "--anime",
            "One Piece",
            "--expected-start",
            "1",
            "--expected-end",
            "1188",
            "--audit-report",
            str(audit_path),
            "--manual-report",
            str(manual_path),
            "--json-report",
            str(certification_path),
        ],
    )

    certify_scope_v3_dataset.main()

    assert certification_path.exists()

    report = json.loads(
        certification_path.read_text(
            encoding="utf-8"
        )
    )

    assert (
        report["certification_status"]
        == "ELIGIBLE"
    )