from selenium.webdriver.common.by import By

from nicegui import __version__
from nicegui.testing import SeleniumScreen


def test_dev_mode(screen: SeleniumScreen) -> None:
    screen.ui_run_kwargs['prod_js'] = False
    screen.open('/')
    screen.selenium.find_element(By.XPATH, f'//script[@src="/_nicegui/{__version__}/static/vue.global.js"]')
    screen.selenium.find_element(By.XPATH, f'//script[@src="/_nicegui/{__version__}/static/quasar.umd.js"]')


def test_prod_mode(screen: SeleniumScreen):
    screen.ui_run_kwargs['prod_js'] = True
    screen.open('/')
    screen.selenium.find_element(By.XPATH, f'//script[@src="/_nicegui/{__version__}/static/vue.global.prod.js"]')
    screen.selenium.find_element(By.XPATH, f'//script[@src="/_nicegui/{__version__}/static/quasar.umd.prod.js"]')
