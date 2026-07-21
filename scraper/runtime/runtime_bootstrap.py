from dataclasses import dataclass

from sqlalchemy.orm import Session

from scraper.runtime.api_service_factory import (
    RuntimeApiMode,
    create_api_service,
)
from scraper.runtime.model_factory import (
    RuntimeModelMode,
    get_models,
)


@dataclass(frozen=True)
class RuntimeBootstrap:
    """
    Fully composed runtime.

    This class is intentionally lightweight. Its purpose is to verify that
    the runtime factories compose correctly while the legacy runtime remains
    the production default.
    """

    models: object
    api_service: object
    mode: RuntimeApiMode


def build_runtime(
    session: Session,
    mode: RuntimeApiMode = RuntimeApiMode.PRODUCTION,
) -> RuntimeBootstrap:
    """
    Compose a complete runtime without changing production wiring.
    """

    model_mode = (
        RuntimeModelMode.PRODUCTION
        if mode is RuntimeApiMode.PRODUCTION
        else RuntimeModelMode.SHARED_MANGA
    )

    return RuntimeBootstrap(
        models=get_models(model_mode),
        api_service=create_api_service(session, mode),
        mode=mode,
    )