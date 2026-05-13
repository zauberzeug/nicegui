from ..logging import log

_shown_warnings: set[str] = set()


def warn_once(message: str, *, stack_info: bool = False) -> None:
    """Print a warning message only once."""
    if message not in _shown_warnings:
        log.warning(message, stack_info=stack_info)
        _shown_warnings.add(message)
