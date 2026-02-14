from ...dependencies import setup_esm_package

__getattr__, __dir__ = setup_esm_package(__file__, __name__, 'nicegui-echart', {'EChart': '.echart'})
__all__ = ['EChart']  # pylint: disable=undefined-all-variable
