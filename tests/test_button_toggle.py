from nicegui import ui
from nicegui.testing import Screen


def test_button_toggle(screen: Screen):
    result_label = ui.label('Selected: Option A')  # Initialize with the initial value
    ui.button_toggle(['Option A', 'Option B', 'Option C'],
                             value='Option A',
                             on_change=lambda e: result_label.set_text(f'Selected: {e.value}'))

    screen.open('/')
    screen.should_contain('Selected: Option A')  # Initial value should be displayed

    # Test clicking different options
    screen.click('Option B')
    screen.should_contain('Selected: Option B')

    screen.click('Option C')
    screen.should_contain('Selected: Option C')

    # Test clicking the same option again (should remain selected)
    screen.click('Option C')
    screen.should_contain('Selected: Option C')


def test_button_toggle_with_dict_options(screen: Screen):
    result_label = ui.label('Selected: 7d')  # Initialize with the initial value
    ui.button_toggle([
        {'label': 'Today', 'value': '1d'},
        {'label': 'This Week', 'value': '7d'},
        {'label': 'This Month', 'value': '30d'},
    ], value='7d', on_change=lambda e: result_label.set_text(f'Selected: {e.value}'))

    screen.open('/')
    screen.should_contain('Selected: 7d')  # Initial value

    screen.click('Today')
    screen.should_contain('Selected: 1d')

    screen.click('This Month')
    screen.should_contain('Selected: 30d')


def test_button_toggle_programmatic_control(screen: Screen):
    result_label = ui.label('Selected: Red')  # Initialize with the initial value
    toggle = ui.button_toggle(['Red', 'Green', 'Blue'],
                             value='Red',
                             on_change=lambda e: result_label.set_text(f'Selected: {e.value}'))

    ui.button('Set Green', on_click=lambda: toggle.set_value('Green'))
    ui.button('Set Blue', on_click=lambda: toggle.set_value('Blue'))

    screen.open('/')
    screen.should_contain('Selected: Red')  # Initial value

    # Test programmatic value setting
    screen.click('Set Green')
    screen.should_contain('Selected: Green')

    screen.click('Set Blue')
    screen.should_contain('Selected: Blue')

    # Test manual clicking after programmatic change
    screen.click('Red')
    screen.should_contain('Selected: Red')
