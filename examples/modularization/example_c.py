import theme
from message import message

from nicegui import APIRouter, ui

router = APIRouter(prefix='/c')


@router.page('/')
def example_page():
    """
    Renders an example page with a frame, a message, and multiple links.

    This function creates a page with a frame titled 'Example C'. It then displays a message
    saying 'Example C'. After that, it creates three links labeled 'Item 1', 'Item 2', and 'Item 3',
    each pointing to a different URL. The links are styled with the classes 'text-xl' and 'text-grey-8'.

    Returns:
        None
    """
    with theme.frame('- Example C -'):
        message('Example C')
        for i in range(1, 4):
            ui.link(f'Item {i}', f'/c/items/{i}').classes('text-xl text-grey-8')


@router.page('/items/{id}', dark=True)
def item(id: str):
    """
    Display an item with the given ID.

    Parameters:
    - id (str): The ID of the item.

    Usage:
    - Call this function to display an item with the specified ID.
    - The item will be displayed within a themed frame.
    - The item's ID will be shown as a message.
    - A link to go back to the previous page will be provided.

    Example:
    >>> item('123')
    """
    with theme.frame(f'- Example C{id} -'):
        message(f'Item  #{id}')
        ui.link('go back', router.prefix).classes('text-xl text-grey-8')
