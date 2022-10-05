from nicegui import ui

from .screen import Screen


def test_rendering_page(screen: Screen):
    ui.label('test label')
    with ui.row().classes('positive'):
        ui.input('test input', placeholder='some placeholder')
    with ui.column():
        ui.label('1')
        ui.label('2')
        ui.label('3')
        with ui.card():
            ui.label('some text')

    screen.open('/')
    assert screen.render_content() == '''Title: NiceGUI

test label
row
  test input: some placeholder
column
  1
  2
  3
  card
    some text
'''

    assert screen.render_content(with_extras=True) == '''Title: NiceGUI

test label
row [class: items-start gap-4 positive]
  test input: some placeholder [class: no-wrap items-start standard labeled]
column [class: items-start gap-4]
  1
  2
  3
  card [class: items-start q-pa-md gap-4]
    some text
'''
