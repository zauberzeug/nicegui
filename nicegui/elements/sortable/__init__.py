from typing import TYPE_CHECKING

from ...dependencies import setup_esm_package

__getattr__, __dir__ = setup_esm_package(__file__, __name__, 'nicegui-sortable', {'Sortable': '.sortable'})
__all__ = ['Sortable']

if TYPE_CHECKING:
    from .sortable import Sortable
