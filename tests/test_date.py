from nicegui import ui
from nicegui.testing import SharedScreen


def test_date(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.date(value='2023-01-01')

    shared_screen.open('/')
    shared_screen.should_contain('Sun, Jan 1')

    shared_screen.click('31')
    shared_screen.should_contain('Tue, Jan 31')


def test_date_with_range(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.date().props('range default-year-month=2023/01')

    shared_screen.open('/')
    shared_screen.click('16')
    shared_screen.click('19')
    shared_screen.should_contain('4 days')

    shared_screen.click('25')
    shared_screen.click('28')
    shared_screen.should_contain('4 days')


def test_date_with_multi_selection(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.date().props('multiple default-year-month=2023/01')

    shared_screen.open('/')
    shared_screen.click('16')
    shared_screen.click('19')
    shared_screen.should_contain('2 days')

    shared_screen.click('25')
    shared_screen.click('28')
    shared_screen.should_contain('4 days')


def test_date_with_range_and_multi_selection(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.date().props('range multiple default-year-month=2023/01')

    shared_screen.open('/')
    shared_screen.click('16')
    shared_screen.click('19')
    shared_screen.should_contain('4 days')

    shared_screen.click('25')
    shared_screen.click('28')
    shared_screen.should_contain('8 days')


def test_date_with_filter(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        d = ui.date().props('''default-year-month=2023/01 :options="date => date <= '2023/01/15'"''')
        ui.label().bind_text_from(d, 'value')

    shared_screen.open('/')
    shared_screen.click('14')
    shared_screen.should_contain('2023-01-14')
    shared_screen.click('15')
    shared_screen.should_contain('2023-01-15')
    shared_screen.click('16')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('2023-01-16')
