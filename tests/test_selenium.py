from .screen import Screen


def test_webdriver():
    from selenium.webdriver import Chrome, ChromeOptions

    chrome_options = ChromeOptions()
    chrome_options.add_argument('--disable-dev-shm-using')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=600x600')
    chrome_driver = Chrome(executable_path='/chromedriver', chrome_options=chrome_options)

    chrome_driver.get('https://www.google.com')
    assert 'Google' in chrome_driver.title

def test_screen_open(screen: Screen):
    screen.open("/")
    assert screen.is_open
    screen.close()

# BUG: this is failing, cannot find "Hello, world!"
def test_screen_should_contain(screen: Screen): 
    from nicegui import ui

    ui.label("Hello, world!")

    screen.open("/")
    assert screen.should_contain("Hello, world!")
    screen.close()