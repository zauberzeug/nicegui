from nicegui import ui

from . import doc


@doc.demo(ui.timeline)
def main_demo() -> None:
    with ui.timeline(side='right'):
        ui.timeline_entry('Rodja and Falko start working on NiceGUI.',
                          title='Initial commit',
                          subtitle='May 07, 2021')
        ui.timeline_entry('The first PyPI package is released.',
                          title='Release of 0.1',
                          subtitle='May 14, 2021')
        ui.timeline_entry('Large parts are rewritten to remove JustPy '
                          'and to upgrade to Vue 3 and Quasar 2.',
                          title='Release of 1.0',
                          subtitle='December 15, 2022',
                          icon='rocket')


doc.reference(ui.timeline)
