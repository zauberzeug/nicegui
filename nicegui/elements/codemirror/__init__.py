from typing import TYPE_CHECKING

from ...dependencies import setup_esm_package

__getattr__, __dir__ = setup_esm_package(
    __file__, __name__, 'nicegui-codemirror',
    {'CodeMirror': '.codemirror', 'Diagnostic': '.codemirror', 'DiagnosticCount': '.codemirror'},
)
__all__ = ['CodeMirror', 'Diagnostic', 'DiagnosticCount']

if TYPE_CHECKING:
    from .codemirror import CodeMirror, Diagnostic, DiagnosticCount
