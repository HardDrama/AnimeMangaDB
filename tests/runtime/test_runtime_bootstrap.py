from sqlalchemy.orm import Session

from scraper.database import models
from scraper.database import models_shared_manga

from scraper.runtime.api_service_factory import RuntimeApiMode
from scraper.runtime.runtime_bootstrap import (
    RuntimeBootstrap,
    build_runtime,
)


def test_build_production_runtime():

    session = Session()

    try:

        runtime = build_runtime(session)

        assert isinstance(runtime, RuntimeBootstrap)
        assert runtime.models is models
        assert runtime.mode is RuntimeApiMode.PRODUCTION

    finally:

        session.close()


def test_build_shared_runtime():

    session = Session()

    try:

        runtime = build_runtime(
            session,
            RuntimeApiMode.SHARED_MANGA,
        )

        assert isinstance(runtime, RuntimeBootstrap)
        assert runtime.models is models_shared_manga
        assert runtime.mode is RuntimeApiMode.SHARED_MANGA

    finally:

        session.close()