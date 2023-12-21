from nicegui import ui

from . import doc


@doc.demo('Tabs', '''
    The elements `ui.tabs`, `ui.tab`, `ui.tab_panels`, and `ui.tab_panel` resemble
    [Quasar's tabs](https://quasar.dev/vue-components/tabs) and
    [tab panels](https://quasar.dev/vue-components/tab-panels>) API.

    `ui.tabs` creates a container for the tabs. This could be placed in a `ui.header` for example.
    `ui.tab_panels` creates a container for the tab panels with the actual content.
    Each `ui.tab_panel` is associated with a `ui.tab` element.
''')
def main_demo() -> None:
    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('One')
        two = ui.tab('Two')
    with ui.tab_panels(tabs, value=two).classes('w-full'):
        with ui.tab_panel(one):
            ui.label('First tab')
        with ui.tab_panel(two):
            ui.label('Second tab')


@doc.demo('Name, label, icon', '''
    The `ui.tab` element has a `label` property that can be used to display a different text than the `name`.
    The `name` can also be used instead of the `ui.tab` objects to associate a `ui.tab` with a `ui.tab_panel`. 
    Additionally each tab can have an `icon`.
''')
def name_and_label():
    with ui.tabs() as tabs:
        ui.tab('h', label='Home', icon='home')
        ui.tab('a', label='About', icon='info')
    with ui.tab_panels(tabs, value='h').classes('w-full'):
        with ui.tab_panel('h'):
            ui.label('Main Content')
        with ui.tab_panel('a'):
            ui.label('Infos')


@doc.demo('Switch tabs programmatically', '''
    The `ui.tabs` and `ui.tab_panels` elements are derived from ValueElement which has a `set_value` method.
    That can be used to switch tabs programmatically.
''')
def switch_tabs():
    content = {'Tab 1': 'Content 1', 'Tab 2': 'Content 2', 'Tab 3': 'Content 3'}
    with ui.tabs() as tabs:
        for title in content:
            ui.tab(title)
    with ui.tab_panels(tabs).classes('w-full') as panels:
        for title, text in content.items():
            with ui.tab_panel(title):
                ui.label(text)

    ui.button('GoTo 1', on_click=lambda: panels.set_value('Tab 1'))
    ui.button('GoTo 2', on_click=lambda: tabs.set_value('Tab 2'))


@doc.demo(
    "Vertical tabs layout",
    """
    Based on [Quasar's vertical tabs](https://quasar.dev/vue-components/tabs#vertical) example,
    we can combine `ui.splitter` and tabs elements to create a vertical tabs layout.
""",
)
def vertical_tabs():
    with ui.splitter(value=20).classes('w-full') as splitter:
        with splitter.before:
            with ui.tabs().props('vertical').classes('w-full') as tabs:
                one = ui.tab('One')
                two = ui.tab('Two')
        with splitter.after:
            with ui.tab_panels(tabs, value=two).classes('w-full'):
                with ui.tab_panel(one):
                    ui.label('First tab')
                with ui.tab_panel(two):
                    ui.label('Second tab')


doc.reference(ui.tabs, title='Reference for ui.tabs')
doc.reference(ui.tabs, title='Reference for ui.tab')
doc.reference(ui.tabs, title='Reference for ui.tab_panels')
doc.reference(ui.tabs, title='Reference for ui.tab_panel')
