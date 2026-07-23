"""Shared machinery for lazily importing module attributes via a PEP 562 module ``__getattr__``."""
import importlib
import sys
from collections.abc import Mapping


def resolve(module_name: str, package: str, lazy_imports: Mapping[str, tuple[str, str | None]], name: str) -> object:
    """Import the attribute ``name`` as declared in ``lazy_imports`` and cache it on module ``module_name``.

    Each entry in ``lazy_imports`` maps an attribute name to a ``(module path, attribute name)`` tuple,
    where the module path is resolved relative to ``package``.
    An empty attribute name yields the module itself.
    """
    if name not in lazy_imports:
        raise AttributeError(f'module {module_name!r} has no attribute {name!r}')
    module_path, attr_name = lazy_imports[name]
    module = importlib.import_module(module_path, package=package)
    value = getattr(module, attr_name) if attr_name else module
    setattr(sys.modules[module_name], name, value)
    return value
