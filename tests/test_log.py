from selenium.webdriver.common.by import By

from nicegui import ui

from .screen import Screen


def test_log(screen: Screen):
    log = ui.log(max_lines=3)
    log.push('A')
    log.push('B')
    log.push('C')
    log.push('D')

    screen.open('/')
    assert screen.selenium.find_element(By.ID, log.id).text == 'B\nC\nD'

    log.clear()
    screen.wait(0.5)
    assert screen.selenium.find_element(By.ID, log.id).text == ''


def test_log_with_newlines(screen: Screen):
    log = ui.log(max_lines=3)
    log.push('A')
    log.push('B')
    log.push('C\nD')

    screen.open('/')
    assert screen.selenium.find_element(By.ID, log.id).text == 'B\nC\nD'
