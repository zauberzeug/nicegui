"""Stub modules for worker subprocesses (see https://github.com/zauberzeug/nicegui/issues/5684).

When a NiceGUI app spawns worker subprocesses (``run.cpu_bound``, ``multiprocessing.Pool``, ``Manager()``, ...),
each worker re-imports the user's main module and thereby the nicegui package.
Workers don't serve UI, so UI-related modules are replaced with no-op stubs which makes the re-import
practically free and turns module-level UI code (``ui.label(...)``, ``ui.run(...)``) into harmless no-ops.

Modules listed in ``REAL_MODULES`` are NOT stubbed:

- ``run`` must be real because unpickling a ``run.cpu_bound`` payload imports it in the worker
- ``native`` must be real because the native-mode window subprocess executes its entry point
- data-bearing modules (``binding``, ``dataclasses``, ``events``, ``observables``, ...) must be real so that
  classes derived from them (e.g. via ``@binding.bindable_dataclass``) keep working in workers,
  including unpickling ``run.cpu_bound`` payloads that reference such classes
- the set is closed under imports (enforced by ``tests/test_worker_stubs.py``):
  a real module must never import from a stubbed one, or it would bind no-op values

Known limitations (by design — workers should not consume UI state):

- worker code that READS values from stubbed modules gets ``WHATEVER`` objects: equality comparisons,
  truthiness and containment are ``False``, iteration is empty — conditions silently take the negative branch
- operations that are not stubbed (``len()``, ``int()``, ``+`` with a real left operand, format specs)
  raise loudly, which is preferable to silent corruption
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
    """A universal no-op object: every operation yields the no-op singleton ``WHATEVER``.

    Truthiness is ``False``, iteration is empty and containment checks are ``False``,
    so conditions and loops over stub values silently take the empty/negative branch.
    """

    def __init__(self, *args, **kwargs) -> None:
        pass  # accept any arguments so that user classes subclassing a stub (via __mro_entries__) can instantiate

    def __getattr__(self, name: str) -> 'Whatever':
        return WHATEVER

    def __call__(self, *args, **kwargs) -> 'Whatever':
        return WHATEVER

    def __mro_entries__(self, *args, **kwargs) -> tuple:  # pylint: disable=unused-argument
        return (Whatever,)  # so module-level `class X(ui.element)` survives class creation

    def __enter__(self) -> 'Whatever':
        return WHATEVER  # so module-level `with ui.row():` no-ops (e.g. examples/menu_and_tabs)

    def __exit__(self, *args) -> Literal[False]:
        return False

    def __getitem__(self, item) -> 'Whatever':
        return WHATEVER  # e.g. generic subscription like Handler[X] in annotations evaluated at class definition

    def __eq__(self, other: object) -> bool:
        return False  # two unrelated stub values must not compare equal just because they share the singleton

    __hash__ = object.__hash__  # would be unset by defining __eq__; identity hashing keeps stubs usable as dict keys

    def __bool__(self) -> bool:
        return False  # so module-level `if app.storage...:` and the like take the negative branch

    def __iter__(self):
        return iter(())  # without this, `__getitem__` would make the legacy sequence protocol iterate forever

    def __contains__(self, item) -> bool:
        return False

    def __repr__(self) -> str:
        return '<nicegui worker stub>'


WHATEVER = Whatever()


class WhateverModule(ModuleType):
    """A module whose every attribute is the ``WHATEVER`` no-op object."""

    def __getattr__(self, name: str) -> Whatever:
        return WHATEVER


def install() -> None:
    """Pre-fill ``sys.modules`` with stubs for all non-essential top-level nicegui modules."""
    for module_info in pkgutil.iter_modules([os.path.dirname(__file__)]):
        name = module_info.name
        if name.startswith('_') or name in REAL_MODULES:
            continue
        sys.modules[f'nicegui.{name}'] = WhateverModule(f'nicegui.{name}')
