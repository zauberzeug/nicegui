import theme
from message import message

from nicegui import APIRouter, ui

# NOTE: the APIRouter does not yet work with NiceGUI On Air (see https://github.com/zauberzeug/nicegui/discussions/2792)
router = APIRouter(prefix='/c')


@router.page('/')
def example_page():
    with theme.frame('- Page C -'):
        message('Page C')
        for i in range(1, 4):
            ui.link(f'Item {i}', f'/c/items/{i}').classes('text-xl text-grey-8')


@router.page('/items/{id}', dark=True)
def item(id: str):
    with theme.frame(f'- Page C{id} -'):
        message(f'Item  #{id}')
        ui.link('go back', router.prefix).classes('text-xl text-grey-8')
