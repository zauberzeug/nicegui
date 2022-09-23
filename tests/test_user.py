from nicegui import ui

from .user import User


def test_rendering_page(user: User):
    ui.label('test label')
    with ui.row().classes('positive'):
        ui.input('test input', placeholder='test placeholder')
    with ui.column():
        ui.label('1')
        ui.label('2')
        ui.label('3')

    user.open('/')
    assert user.page() == '''Title: NiceGUI

test label
row
  test input: test placeholder
column
  1
  2
  3
'''
