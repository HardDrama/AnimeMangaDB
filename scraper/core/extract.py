from scraper.core.selector_engine import SelectorEngine


def required_text(
    engine: SelectorEngine,
    selector_name: str,
) -> str:
    """
    Return required text or raise an exception.
    """

    value = engine.get_text(selector_name)

    if value is None:
        raise ValueError(
            f"Missing required selector '{selector_name}'"
        )

    return value