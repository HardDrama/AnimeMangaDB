from scraper.database import models
from scraper.database import models_shared_manga


class RuntimeModelProvider:
    """
    Centralized access to ORM implementations.

    During the compatibility phase, production code continues
    using the legacy ORM while staged implementations remain
    available for isolated validation.
    """

    production = models
    staged = models_shared_manga