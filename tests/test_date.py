from nicegui import ui
from nicegui.testing import Screen


def test_date(screen: Screen):
    ui.date(value='2023-01-01')

    screen.open('/')
    screen.should_contain('Sun, Jan 1')

    screen.click('31')
    screen.should_contain('Tue, Jan 31')


def test_date_with_range(screen: Screen):
    ui.date().props('range default-year-month=2023/01')

    screen.open('/')
    screen.click('16')
    screen.click('19')
    screen.should_contain('4 days')

    screen.click('25')
    screen.click('28')
    screen.should_contain('4 days')


def test_date_with_multi_selection(screen: Screen):
    ui.date().props('multiple default-year-month=2023/01')

    screen.open('/')
    screen.click('16')
    screen.click('19')
    screen.should_contain('2 days')

    screen.click('25')
    screen.click('28')
    screen.should_contain('4 days')


def test_date_with_range_and_multi_selection(screen: Screen):
    ui.date().props('range multiple default-year-month=2023/01')

    screen.open('/')
    screen.click('16')
    screen.click('19')
    screen.should_contain('4 days')

    screen.click('25')
    screen.click('28')
    screen.should_contain('8 days')


def test_date_with_filter(screen: Screen):
    d = ui.date().props('''default-year-month=2023/01 :options="date => date <= '2023/01/15'"''')
    ui.label().bind_text_from(d, 'value')

    screen.open('/')
    screen.click('14')
    screen.should_contain('2023-01-14')
    screen.click('15')
    screen.should_contain('2023-01-15')
    screen.click('16')
    screen.wait(0.5)
    screen.should_not_contain('2023-01-16')
