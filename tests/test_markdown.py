from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen


def test_markdown(screen: Screen):
    @ui.page('/')
    def page():
        m = ui.markdown('This is **Markdown**')
        ui.button('Set new content', on_click=lambda: m.set_content('New **content**'))

    screen.open('/')
    element = screen.find('This is')
    assert element.text == 'This is Markdown'
    assert element.get_attribute('innerHTML') == 'This is <strong>Markdown</strong>'

    screen.click('Set new content')
    element = screen.find('New')
    assert element.text == 'New content'
    assert element.get_attribute('innerHTML') == 'New <strong>content</strong>'


def test_markdown_with_mermaid(screen: Screen):
    m = None

    @ui.page('/')
    def page():
        nonlocal m
        m = ui.markdown('''
            Mermaid:

            ```mermaid
            graph TD;
                Node_A --> Node_B;
            ```
        ''', extras=['mermaid', 'fenced-code-blocks'])
        ui.button('Set new content', on_click=lambda: m.set_content('''
            New:

            ```mermaid
            graph TD;
                Node_C --> Node_D;
            ```
        '''))

    screen.open('/')
    screen.should_contain('Mermaid')
    screen.wait(1.0)  # wait for Mermaid to render
    assert screen.find_by_tag('svg').get_attribute('id') == f'{m.html_id}_mermaid_0'
    _wait_for_xpath_displayed(screen, '//span[p[contains(text(), "Node_A")]]')

    screen.click('Set new content')
    screen.should_contain('New')
    _wait_for_xpath_displayed(screen, '//span[p[contains(text(), "Node_C")]]')
    screen.should_not_contain('Node_A')


def test_markdown_with_mermaid_on_demand(screen: Screen):
    @ui.page('/')
    def page():
        ui.button('Create Mermaid', on_click=lambda: ui.markdown('''
            ```mermaid
            graph TD;
                Node_A --> Node_B;
            ```
        ''', extras=['mermaid', 'fenced-code-blocks']))

    screen.open('/')
    screen.click('Create Mermaid')
    _wait_for_xpath_displayed(screen, '//span[p[contains(text(), "Node_A")]]')
    _wait_for_xpath_displayed(screen, '//span[p[contains(text(), "Node_B")]]')


def test_strip_indentation(screen: Screen):
    @ui.page('/')
    def page():
        ui.markdown('''
            **This is Markdown.**
        ''')

    screen.open('/')
    screen.should_contain('This is Markdown.')
    screen.should_not_contain('**This is Markdown.**')  # NOTE: '**' are translated to formatting and not visible


def test_replace_markdown(screen: Screen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.markdown('A')

        def replace():
            container.clear()
            with container:
                ui.markdown('B')
        ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('A')

    screen.click('Replace')
    screen.should_contain('B')
    screen.should_not_contain('A')


def _wait_for_xpath_displayed(screen: Screen, xpath: str, attempts: int = 5, delay: float = 0.2):
    for _ in range(attempts):
        try:
            el = screen.selenium.find_element(By.XPATH, xpath)
            if el.is_displayed():
                return el
        except Exception:
            pass
        screen.wait(delay)
    raise AssertionError(f'{xpath} not displayed')
