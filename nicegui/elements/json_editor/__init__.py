from typing import TYPE_CHECKING

from ...dependencies import setup_esm_package

__getattr__, __dir__ = setup_esm_package(__file__, __name__, 'nicegui-json-editor', {'JsonEditor': '.json_editor'})
__all__ = ['JsonEditor']

if TYPE_CHECKING:
    from .json_editor import JsonEditor
