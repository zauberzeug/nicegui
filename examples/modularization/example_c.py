import theme
from message import message

from nicegui import APIRouter, ui

router = APIRouter(prefix='/c')


@router.page('/')
def example_page():
    with theme.frame('- Example C -'):
        message('Example C')
        for i in range(1, 4):
            ui.link(f'Item {i}', f'/c/items/{i}').classes('text-xl text-grey-8')


@router.page('/items/{id}', dark=True)
def item(id: str):
    with theme.frame(f'- Example C{id} -'):
        message(f'Item  #{id}')
        ui.link('go back', router.prefix).classes('text-xl text-grey-8')
