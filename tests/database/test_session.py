from sqlalchemy import text

from scraper.database.session import engine


def test_sqlite_foreign_keys_are_enabled():
    with engine.connect() as connection:
        enabled = connection.execute(
            text("PRAGMA foreign_keys")
        ).scalar_one()

    assert enabled == 1