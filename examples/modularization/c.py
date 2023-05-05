import theme

from nicegui import APIRouter, ui

router = APIRouter()


@router.page('/c')
def example_page():
    with theme.frame('- Example C -'):
        ui.label('Example C').classes('text-h4 text-grey-8')
