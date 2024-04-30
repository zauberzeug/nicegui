import theme
from message import message

from nicegui import APIRouter, ui

# NOTE: the APIRouter does not yet work with NiceGUI On Air (see https://github.com/zauberzeug/nicegui/discussions/2792)
router = APIRouter(prefix='/c')


@router.page('/')
def example_page():
    with theme.frame('- Page C -'):
        message('Page C')
        ui.label('This page and its subpages are created using an APIRouter.')
        ui.link('Item 1', '/c/items/1').classes('text-xl text-grey-8')
        ui.link('Item 2', '/c/items/2').classes('text-xl text-grey-8')
        ui.link('Item 3', '/c/items/3').classes('text-xl text-grey-8')


@router.page('/items/{item_id}', dark=True)
def item(item_id: str):
    with theme.frame(f'- Page C{item_id} -'):
        message(f'Item  #{item_id}')
        ui.link('go back', router.prefix).classes('text-xl text-grey-8')
