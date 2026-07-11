import sys

from tools import audit_scope_v2


def test_audit_defaults_to_one_piece(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        sys,
        "argv",
        ["audit_scope_v2"],
    )

    audit_scope_v2.main()

    output = capsys.readouterr().out

    assert "Anime: One Piece" in output


def test_audit_supports_anime_selection(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "audit_scope_v2",
            "--anime",
            "Naruto",
        ],
    )

    audit_scope_v2.main()

    output = capsys.readouterr().out

    assert "Anime: Naruto" in output


def test_audit_reports_missing_anime(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "audit_scope_v2",
            "--anime",
            "Does Not Exist",
        ],
    )

    audit_scope_v2.main()

    output = capsys.readouterr().out

    assert (
        'Anime not found: "Does Not Exist"'
        in output
    )

def test_naruto_audit_applies_arc_exceptions(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "audit_scope_v2",
            "--anime",
            "Naruto",
        ],
    )

    audit_scope_v2.main()

    output = capsys.readouterr().out

    assert "Arc Not Applicable: 14" in output
    assert "Unresolved Arc Gaps: 0" in output
    assert "Effective Arc Completion: 100.00%" in output
    assert "Audit Status     : PASS" in output