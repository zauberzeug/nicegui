from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains

from nicegui import ui
from nicegui.testing import Screen


def test_init(screen: Screen) -> None:
    @ui.page('/')
    async def main():
        default_terminal = ui.xterm()
        custom_terminal = ui.xterm({'cols': 132, 'rows': 43})
        await ui.context.client.connected()

        ui.label(f'Default terminal size: {await default_terminal.get_columns()}x{await default_terminal.get_rows()}')
        ui.label(f'Custom terminal size: {await custom_terminal.get_columns()}x{await custom_terminal.get_rows()}')

    screen.open('/')
    screen.should_contain('Default terminal size: 80x24')  # See https://softwareengineering.stackexchange.com/q/148754
    screen.should_contain('Custom terminal size: 132x43')


def test_write(screen: Screen) -> None:
    @ui.page('/')
    def main():
        terminal = ui.xterm()
        ui.button('Write Hello!', on_click=lambda: terminal.write('Hello!'))
        ui.button('Write 😎', on_click=lambda: terminal.write(b'\xf0\x9f\x98\x8e\n\r'))
        ui.button('Write link', on_click=lambda: terminal.writeln(f'http://localhost:{screen.PORT}/subpage'))

    @ui.page('/subpage')
    def subpage():
        ui.label('This is the subpage')

    screen.open('/')
    screen.click('Write Hello!')
    screen.click('Write 😎')
    screen.wait(0.1)
    assert screen.find_by_class('xterm').text == 'Hello!😎\n '

    # `Ctrl`+ click on a link opens the link in a new tab
    screen.click('Write link')
    link = screen.find('subpage')
    ActionChains(screen.selenium).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
    screen.switch_to(1)  # Switch to the new tab opened by the link
    screen.should_contain('This is the subpage')


def test_bell_and_data_events(screen: Screen) -> None:
    counts = {'bell': 0, 'data': 0}

    @ui.page('/')
    def main():
        terminal = ui.xterm()
        terminal.on_bell(lambda: counts.update(bell=counts['bell'] + 1))
        terminal.on_data(lambda: counts.update(data=counts['data'] + 1))
        ui.button('Ring Bell', on_click=lambda: terminal.write('\x07'))
        ui.button('Input 456', on_click=lambda: terminal.input('456'))

    screen.open('/')
    screen.click('Ring Bell')
    screen.wait(0.1)
    assert counts == {'bell': 1, 'data': 0}

    screen.find_by_class('xterm').click()
    screen.type('123')
    screen.click('Input 456')
    screen.wait(0.1)
    assert counts == {'bell': 1, 'data': 4}  # The `input` method triggers a single data event
    screen.should_not_contain('123456')  # Neither typing nor the `input` method write text on the terminal


def test_fit_and_other_events(screen: Screen) -> None:
    @ui.page('/')
    def main():
        with ui.card().classes('size-96'):
            terminal = ui.xterm()
            terminal.on('resize', lambda e: ui.label(f'Terminal size: {e.args["cols"]}x{e.args["rows"]}'))
            ui.button('Fill', on_click=lambda: terminal.classes('size-full'))
            ui.button('Fit', on_click=terminal.fit)

    screen.open('/')
    screen.click('Fill')
    screen.click('Fit')
    screen.should_contain('Terminal size: 37x19')  # depends on size of the container (ui.card)


def test_run_terminal_method(screen: Screen) -> None:
    @ui.page('/')
    async def main():
        terminal = ui.xterm({'rows': 4})
        await ui.context.client.connected()
        await terminal.write('\n\n\n' + 'Hello NiceGUI!' + '\n\r' + 'https://nicegui.io/' + '\n\n\n\n')

        await terminal.run_terminal_method('scrollLines', -2)  # Scroll up 2 lines
        await terminal.run_terminal_method(':select', '8', 'this.rows', '10')  # 10 chars starting at column 8, row 4
        ui.label(f'Selected text: {await terminal.run_terminal_method("getSelection")}')

    screen.open('/')
    screen.should_contain('Hello NiceGUI!')
    screen.should_contain('Selected text: nicegui.io')
