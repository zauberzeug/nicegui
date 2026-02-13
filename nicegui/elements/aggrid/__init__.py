from ...dependencies import setup_esm_package

__getattr__, __dir__ = setup_esm_package(__file__, __name__, 'nicegui-aggrid', {'AgGrid': '.aggrid'})
__all__ = ['AgGrid']
