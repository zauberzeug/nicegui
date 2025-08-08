from typing import List

from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains

from nicegui import ui
from nicegui.events import XtermBellEventArguments, XtermDataEventArguments
from nicegui.testing import Screen


def test_init(screen: Screen) -> None:
    @ui.page('/')
    async def main():
        terminal_default = ui.xterm()
        custom_size = ui.xterm({'cols': 132, 'rows': 43})
        await ui.context.client.connected()

        ui.label(f'Default terminal size: {await terminal_default.get_columns()}x{await terminal_default.get_rows()}')
        ui.label(f'Custom terminal size: {await custom_size.get_columns()}x{await custom_size.get_rows()}')

    screen.open('/')
    screen.should_contain('Default terminal size: 80x24')  # See https://softwareengineering.stackexchange.com/q/148754
    screen.should_contain('Custom terminal size: 132x43')


def test_write(screen: Screen) -> None:
    terminal = ui.xterm()
    screen.open('/')

    terminal.write('Hello nicegui!')  # write string
    terminal.write(b'\xf0\x9f\x98\x8e\n\r')  # write UTF-8 encoded bytes
    screen.wait(0.1)
    assert screen.find_element(terminal).text.strip() == 'Hello nicegui!😎'

    # `Ctrl`+ click on a link opens the link in a new tab
    terminal.writeln('https://nicegui.io/')
    link = screen.find('https://nicegui.io/')
    ActionChains(screen.selenium).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
    screen.switch_to(1)  # Switch to the new tab opened by the link
    screen.wait(0.5)
    assert screen.selenium.current_url == 'https://nicegui.io/'


def test_bell_and_data_events(screen: Screen) -> None:
    terminal = ui.xterm()
    bell_events: List[XtermBellEventArguments] = []
    data_events: List[XtermDataEventArguments] = []
    terminal.on_bell(bell_events.append)
    terminal.on_data(data_events.append)
    screen.open('/')

    # Write the "Bell" character to trigger bell
    terminal.write('\x07')
    screen.wait(0.1)
    assert len(bell_events) == 1
    assert len(data_events) == 0  # The `write` method does not trigger a data event

    # Type text to trigger data input
    screen.find_element(terminal).click()  # Focus the terminal
    screen.type('Hello ')
    terminal.input('nicegui!')  # The `input` method does trigger a data event
    screen.wait(0.1)
    assert ''.join(e.data for e in data_events) == 'Hello nicegui!'
    screen.should_not_contain('Hello nicegui!')  # Neither typing nor the `input` method write text on the terminal


def test_fit_and_other_events(screen: Screen) -> None:
    with ui.card().classes('size-96'):
        terminal = ui.xterm()

    terminal.on('resize', lambda e: ui.label(f'Terminal size: {e.args["cols"]}x{e.args["rows"]}'))
    screen.open('/')

    terminal.classes('size-full')  # Make the terminal fill its container
    terminal.fit()  # Resize the terminal (number of rows and columns) to fit in the container
    screen.should_contain('Terminal size: 37x19')  # depends on size of the container (ui.card)


def test_run_terminal_method(screen: Screen) -> None:
    @ui.page('/')
    async def main():
        terminal = ui.xterm({'rows': 4})
        await ui.context.client.connected()
        await terminal.write('\n\n\n' + 'Hello nicegui!' + '\n\r' + 'https://nicegui.io/' + '\n\n\n\n')

        await terminal.run_terminal_method('scrollLines', -2)  # Scroll up 2 lines
        await terminal.run_terminal_method(':select', '8', 'this.rows', '10')  # 10 chars starting at column 8, row 4
        ui.label(f'Selected text: {await terminal.run_terminal_method("getSelection")}')

    screen.open('/')
    screen.should_contain('Hello nicegui!')
    screen.should_contain('Selected text: nicegui.io')
