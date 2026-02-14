from ...dependencies import setup_esm_package

__getattr__, __dir__ = setup_esm_package(__file__, __name__, 'nicegui-mermaid', {'Mermaid': '.mermaid'})
__all__ = ['Mermaid']  # pylint: disable=undefined-all-variable
