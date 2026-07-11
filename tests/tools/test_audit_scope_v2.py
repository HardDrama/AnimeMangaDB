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