from sqlalchemy.orm import Session

from scraper.runtime.api_service_factory import (
    RuntimeApiMode,
    create_api_service,
)
from scraper.services.shared_manga_api_service import (
    SharedMangaApiService,
)


def test_factory_builds_production_service():

    session = Session()

    try:

        service = create_api_service(session)

        assert isinstance(
            service,
            SharedMangaApiService,
        )

    finally:

        session.close()


def test_factory_builds_shared_runtime_service():

    session = Session()

    try:

        service = create_api_service(
            session,
            RuntimeApiMode.SHARED_MANGA,
        )

        assert isinstance(
            service,
            SharedMangaApiService,
        )

    finally:

        session.close()


def test_factory_defaults_to_production():

    session = Session()

    try:

        service = create_api_service(session)

        assert isinstance(
            service,
            SharedMangaApiService,
        )

    finally:

        session.close()