from enum import Enum

from scraper.runtime.model_provider import RuntimeModelProvider


class RuntimeModelMode(str, Enum):
    PRODUCTION = "production"
    SHARED_MANGA = "shared_manga"


def get_models(
    mode: RuntimeModelMode = RuntimeModelMode.PRODUCTION,
):
    """
    Return the ORM module for the selected runtime.

    During mitigation this simply exposes the
    appropriate validated model module.
    """

    if mode is RuntimeModelMode.PRODUCTION:
        return RuntimeModelProvider.production

    return RuntimeModelProvider.staged