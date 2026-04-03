from typing import TYPE_CHECKING

from ...dependencies import setup_esm_package

__getattr__, __dir__ = setup_esm_package(__file__, __name__, 'nicegui-xterm', {'Xterm': '.xterm'})
__all__ = ['Xterm']

if TYPE_CHECKING:
    from .xterm import Xterm
