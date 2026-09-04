from .helpers import warn_once

# DEPRECATED: This module will be removed in NiceGUI 4.0


def __getattr__(name: str) -> dict:
    if name == 'KWONLY_SLOTS':
        warn_once('nicegui.dataclasses.KWONLY_SLOTS is deprecated, use kw_only=True, slots=True directly')
        return {'kw_only': True, 'slots': True}
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
