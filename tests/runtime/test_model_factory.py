from scraper.database import models
from scraper.database import models_shared_manga

from scraper.runtime.model_factory import (
    RuntimeModelMode,
    get_models,
)


def test_default_runtime_is_production():

    assert (
        get_models()
        is models
    )


def test_production_runtime():

    assert (
        get_models(
            RuntimeModelMode.PRODUCTION
        )
        is models
    )


def test_shared_runtime():

    assert (
        get_models(
            RuntimeModelMode.SHARED_MANGA
        )
        is models_shared_manga
    )