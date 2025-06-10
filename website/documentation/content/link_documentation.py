from nicegui import ui

from ...style import link_target
from . import doc


@doc.demo(ui.link)
def main_demo() -> None:
    ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')


@doc.demo('Navigate on large pages', '''
    To jump to a specific location within a page you can place linkable anchors with `ui.link_target('target_name')`
    or simply pass a NiceGUI element as link target.
''')
def same_page_links():
    navigation = ui.row()
    # ui.link_target('target_A')
    link_target('target_A', '-10px')  # HIDE
    ui.label(
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, '
        'sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    )
    link_target('target_B', '70px')  # HIDE
    label_B = ui.label(
        'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. '
        'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. '
        'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    )
    with navigation:
        ui.link('Goto A', '#target_A')
        # ui.link('Goto B', label_B)
        ui.link('Goto B', '#target_B')  # HIDE


@doc.auto_execute
@doc.demo('Links to other pages', '''
    You can link to other pages by providing the link target as path or function reference.
''')
def link_to_other_page():
    @ui.page('/some_other_page')
    def my_page():
        ui.label('This is another page')

    ui.label('Go to other page')
    ui.link('... with path', '/some_other_page')
    ui.link('... with function reference', my_page)


@doc.demo('Link from images and other elements', '''
    By nesting elements inside a link you can make the whole element clickable.
    This works with all elements but is most useful for non-interactive elements like
    [ui.image](/documentation/image), [ui.avatar](/documentation/image) etc.
''')
def link_from_elements():
    with ui.link(target='https://github.com/zauberzeug/nicegui'):
        ui.image('https://picsum.photos/id/41/640/360').classes('w-64')


doc.reference(ui.link)
