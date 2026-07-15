from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///animemanga.db"


engine = create_engine(
    DATABASE_URL,
    echo=True,
)


@event.listens_for(
    engine,
    "connect",
)
def enable_sqlite_foreign_keys(
    dbapi_connection,
    connection_record,
):
    del connection_record

    cursor = dbapi_connection.cursor()

    try:
        cursor.execute(
            "PRAGMA foreign_keys=ON"
        )
    finally:
        cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)