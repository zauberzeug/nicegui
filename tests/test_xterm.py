from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains

from nicegui import ui
from nicegui.testing import SharedScreen


def test_init(shared_screen: SharedScreen) -> None:
    @ui.page('/')
    async def main():
        default_terminal = ui.xterm()
        custom_terminal = ui.xterm({'cols': 132, 'rows': 43})
        await ui.context.client.connected()

        ui.label(f'Default terminal size: {await default_terminal.get_columns()}x{await default_terminal.get_rows()}')
        ui.label(f'Custom terminal size: {await custom_terminal.get_columns()}x{await custom_terminal.get_rows()}')

    shared_screen.open('/')
    shared_screen.should_contain('Default terminal size: 80x24')  # See https://softwareengineering.stackexchange.com/q/148754
    shared_screen.should_contain('Custom terminal size: 132x43')


def test_write(shared_screen: SharedScreen) -> None:
    @ui.page('/')
    def main():
        terminal = ui.xterm()
        ui.button('Write Hello!', on_click=lambda: terminal.write('Hello!'))
        ui.button('Write 😎', on_click=lambda: terminal.write(b'\xf0\x9f\x98\x8e\n\r'))
        ui.button('Write link', on_click=lambda: terminal.writeln(f'http://localhost:{shared_screen.PORT}/subpage'))

    @ui.page('/subpage')
    def subpage():
        ui.label('This is the subpage')

    shared_screen.open('/')
    shared_screen.click('Write Hello!')
    shared_screen.click('Write 😎')
    shared_screen.wait(0.1)
    assert shared_screen.find_by_class('xterm').text == 'Hello!😎\n '

    # `Ctrl`+ click on a link opens the link in a new tab
    shared_screen.click('Write link')
    link = shared_screen.find('subpage')
    ActionChains(shared_screen.selenium).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
    shared_screen.switch_to(1)  # Switch to the new tab opened by the link
    shared_screen.should_contain('This is the subpage')


def test_bell_and_data_events(shared_screen: SharedScreen) -> None:
    counts = {'bell': 0, 'data': 0}

    @ui.page('/')
    def main():
        terminal = ui.xterm()
        terminal.on_bell(lambda: counts.update(bell=counts['bell'] + 1))
        terminal.on_data(lambda: counts.update(data=counts['data'] + 1))
        ui.button('Ring Bell', on_click=lambda: terminal.write('\x07'))
        ui.button('Input 456', on_click=lambda: terminal.input('456'))

    shared_screen.open('/')
    shared_screen.click('Ring Bell')
    shared_screen.wait(0.1)
    assert counts == {'bell': 1, 'data': 0}

    shared_screen.find_by_class('xterm').click()
    shared_screen.type('123')
    shared_screen.click('Input 456')
    shared_screen.wait(0.1)
    assert counts == {'bell': 1, 'data': 4}  # The `input` method triggers a single data event
    shared_screen.should_not_contain('123456')  # Neither typing nor the `input` method write text on the terminal


def test_fit_and_resize_event(shared_screen: SharedScreen) -> None:
    @ui.page('/')
    def main():
        with ui.card().classes('size-96'):
            terminal = ui.xterm()
            terminal.on('resize', lambda e: ui.notify(f'Size: {e.args["cols"]}x{e.args["rows"]}'))
        ui.button('Fill', on_click=lambda: terminal.classes('size-full'))
        ui.button('Fit', on_click=terminal.fit)

    shared_screen.open('/')
    shared_screen.click('Fill')
    shared_screen.click('Fit')
    shared_screen.should_contain('Size: 37x20')  # depends on size of the container (ui.card)


def test_run_terminal_method(shared_screen: SharedScreen) -> None:
    @ui.page('/')
    async def main():
        terminal = ui.xterm({'rows': 4})
        await ui.context.client.connected()
        await terminal.write('\n\n\n' + 'Hello NiceGUI!' + '\n\r' + 'https://nicegui.io/' + '\n\n\n\n')

        await terminal.run_terminal_method('scrollLines', -2)  # Scroll up 2 lines
        await terminal.run_terminal_method(':select', '8', 'this.rows', '10')  # 10 chars starting at column 8, row 4
        ui.label(f'Selected text: {await terminal.run_terminal_method("getSelection")}')

    shared_screen.open('/')
    shared_screen.should_contain('Hello NiceGUI!')
    shared_screen.should_contain('Selected text: nicegui.io')
