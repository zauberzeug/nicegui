"""Stub modules for worker subprocesses (see https://github.com/zauberzeug/nicegui/issues/5684).

When a NiceGUI app spawns worker subprocesses (``run.cpu_bound``, ``multiprocessing.Pool``, ``Manager()``, ...),
each worker re-imports the user's main module and thereby the nicegui package.
Workers don't serve UI, so UI-related modules are replaced with no-op stubs which makes the re-import
practically free and turns module-level UI code (``ui.label(...)``, ``ui.run(...)``) into harmless no-ops.

Modules listed in ``REAL_MODULES`` are NOT stubbed:

- ``run`` must be real because unpickling a ``run.cpu_bound`` payload imports it in the worker
- ``native`` must be real because the native-mode window subprocess executes its entry point
- data-bearing modules (``binding``, ``dataclasses``, ``event``, ``events``, ``observables``, ...) must be real so that
  classes derived from them (e.g. via ``@binding.bindable_dataclass``) keep working in workers,
  including unpickling ``run.cpu_bound`` payloads that reference such classes
- the set is closed under imports (enforced by ``tests/test_worker_stubs.py``):
  a real module must never import from a stubbed one, or it would bind no-op values

Known limitations (by design — workers should not consume UI state):

- module-level UI construction (``ui.label(...)``, ``with ui.row():``, ``ui.run()``) silently no-ops
- worker code that READS values from stubbed modules gets stub objects: equality comparisons and containment are
  ``False``, iteration is empty, item assignment is discarded
- truthiness (``if app.storage.user:``) raises a ``TypeError`` naming the attribute, because silently taking the
  negative branch would decide for the user; the one exception is ``core.app.is_stopping``, which is ``False``
  so that ``run.io_bound`` and ``run.cpu_bound`` keep working in workers
- other operations that are not stubbed (``len()``, ``int()``, ``+`` with a real left operand, format specs)
  raise loudly as well, which is preferable to silent corruption
- ``import nicegui.elements.button``-style submodule imports and ``from nicegui import App``-style lazy
  attributes of stubbed submodules raise ``ModuleNotFoundError`` in stub mode (``from nicegui import ui`` works)
- ``nicegui.testing`` is stubbed, which is fine: the pytest plugin loads in pytest's main process, never in workers
- ``fork``-started children (Linux <= 3.13 default) inherit the parent's real modules, so stubs never engage
  there — no benefit, but also no cost, since fork does not re-import anything
"""
import os
import pkgutil
import sys
from types import ModuleType
from typing import Literal

REAL_MODULES = {
    'awaitable_response',
    'background_tasks',
    'binding',
    'context',
    'core',
    'dataclasses',
    'event',
    'events',
    'helpers',
    'json',
    'logging',
    'native',
    'observables',
    'optional_features',
    'run',
    'slot',
    'version',
}


class Whatever:
    """A universal no-op object: attributes are stubs named after the attribute, calls return the stub itself.

    Iteration is empty and containment checks are ``False``, but truthiness raises a ``TypeError``.
    """
    _stub_name = 'value'  # class default, so that instances of user subclasses have one without __getattr__

    def __init__(self, *args, **kwargs) -> None:
        pass  # accept any arguments so that user classes subclassing a stub (via __mro_entries__) can instantiate

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__()  # swallow class keywords like `class X(ui.element, component='x.js')`

    def __getattr__(self, name: str) -> 'Whatever':
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError(name)  # e.g. a stub `__setstate__` would swallow the state of unpickled instances
        return _named(f'{self._stub_name}.{name}')

    def __call__(self, *args, **kwargs) -> 'Whatever':
        return self

    def __mro_entries__(self, *args, **kwargs) -> tuple:  # pylint: disable=unused-argument
        return (Whatever,)  # so module-level `class X(ui.element)` survives class creation

    def __enter__(self) -> 'Whatever':
        return self  # so module-level `with ui.row():` no-ops (e.g. examples/menu_and_tabs)

    def __exit__(self, *args) -> Literal[False]:
        return False

    def __getitem__(self, item) -> 'Whatever':
        return self  # e.g. generic subscription like Handler[X] in annotations evaluated at class definition

    def __setitem__(self, key, value) -> None:
        pass  # e.g. `self._props['value'] = ...` in a custom element instantiated at module level

    def __eq__(self, other: object) -> bool:
        return False  # two unrelated stub values must not compare equal just because they share the singleton

    __hash__ = object.__hash__  # would be unset by defining __eq__; identity hashing keeps stubs usable as dict keys

    def __bool__(self) -> bool:
        raise TypeError(f'{self._stub_name} has no truth value in a worker process, where NiceGUI is stubbed '
                        '(see https://github.com/zauberzeug/nicegui/issues/5684)')

    def __iter__(self):
        return iter(())  # without this, `__getitem__` would make the legacy sequence protocol iterate forever

    def __contains__(self, item) -> bool:
        return False

    def __repr__(self) -> str:
        return '<nicegui worker stub>'


def _named(name: str, **attributes: object) -> Whatever:
    stub = Whatever()
    vars(stub).update(_stub_name=name, **attributes)
    return stub


class WhateverModule(ModuleType):
    """A module whose every attribute is a ``Whatever`` no-op object."""

    def __getattr__(self, name: str) -> Whatever:
        return _named(f'{self.__name__.rsplit(".", 1)[-1]}.{name}')


def install() -> None:
    """Pre-fill ``sys.modules`` with stubs for all non-essential top-level nicegui modules."""
    for module_info in pkgutil.iter_modules([os.path.dirname(__file__)]):
        name = module_info.name
        if name.startswith('_') or name in REAL_MODULES:
            continue
        sys.modules[f'nicegui.{name}'] = WhateverModule(f'nicegui.{name}')
    # the real `run._run` reads `core.app.is_stopping` as a bool, so it must not raise like other stub truthiness
    sys.modules['nicegui.nicegui'].app = _named('app', is_stopping=False)  # type: ignore[attr-defined]
