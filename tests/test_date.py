from nicegui import ui

from .screen import Screen


def test_date(screen: Screen):
    ui.date(value='2023-01-01')

    screen.open('/')
    screen.should_contain('Sun, Jan 1')

    screen.click('31')
    screen.should_contain('Tue, Jan 31')


def test_date_with_range(screen: Screen):
    ui.date().props('range')

    screen.open('/')
    screen.click('16')
    screen.click('19')
    screen.should_contain('4 days')

    screen.click('25')
    screen.click('28')
    screen.should_contain('4 days')


def test_date_with_multi_selection(screen: Screen):
    ui.date().props('multiple')

    screen.open('/')
    screen.click('16')
    screen.click('19')
    screen.should_contain('2 days')

    screen.click('25')
    screen.click('28')
    screen.should_contain('4 days')


def test_date_with_range_and_multi_selection(screen: Screen):
    ui.date().props('range multiple')

    screen.open('/')
    screen.click('16')
    screen.click('19')
    screen.should_contain('4 days')

    screen.click('25')
    screen.click('28')
    screen.should_contain('8 days')
