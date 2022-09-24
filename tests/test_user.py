from nicegui import ui

from .user import User


def test_rendering_page(user: User):
    ui.label('test label')
    with ui.row().classes('positive'):
        ui.input('test input', placeholder='some placeholder')
    with ui.column():
        ui.label('1')
        ui.label('2')
        ui.label('3')
    with ui.card():
        ui.label('some text')

    user.open('/')
    assert user.page() == '''Title: NiceGUI

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

    assert user.page(with_extras=True) == '''Title: NiceGUI

test label
row [class: items-start positive]
  test input: some placeholder [class: no-wrap items-start standard labeled]
column [class: items-start]
  1
  2
  3
card [class: items-start q-pa-md]
  some text
'''
