import theme

from nicegui import APIRouter, ui

router = APIRouter(prefix='/c')


@router.page('/')
def example_page():
    with theme.frame('- Example C -'):
        ui.label('Example C').classes('text-h4 text-grey-8')
        for i in range(1, 4):
            ui.link(f'Item {i}', f'/c/items/{i}').classes('text-xl text-grey-8')


@router.page('/items/{id}', dark=True)
def item(id: str):
    with theme.frame(f'- Example C{id} -'):
        ui.label(f'Item  #{id}').classes('text-h4 text-grey-8')
        ui.link('go back', router.prefix).classes('text-xl text-grey-8')
