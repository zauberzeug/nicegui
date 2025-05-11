from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen


def test_markdown(screen: Screen):
    m = ui.markdown('This is **Markdown**')

    screen.open('/')
    element = screen.find('This is')
    assert element.text == 'This is Markdown'
    assert element.get_attribute('innerHTML') == 'This is <strong>Markdown</strong>'

    m.set_content('New **content**')
    element = screen.find('New')
    assert element.text == 'New content'
    assert element.get_attribute('innerHTML') == 'New <strong>content</strong>'


def test_markdown_with_mermaid(screen: Screen):
    m = ui.markdown('''
        Mermaid:

        ```mermaid
        graph TD;
            Node_A --> Node_B;
        ```
    ''', extras=['mermaid', 'fenced-code-blocks'])

    screen.open('/')
    screen.wait(0.5)  # wait for Mermaid to render
    screen.should_contain('Mermaid')
    assert screen.find_by_tag('svg').get_attribute('id') == f'{m.html_id}_mermaid_0'
    assert screen.selenium.find_element(By.XPATH, '//span[p[contains(text(), "Node_A")]]').is_displayed()

    m.set_content('''
        New:

        ```mermaid
        graph TD;
            Node_C --> Node_D;
        ```
    ''')
    screen.should_contain('New')
    assert screen.selenium.find_element(By.XPATH, '//span[p[contains(text(), "Node_C")]]').is_displayed()
    screen.should_not_contain('Node_A')


def test_markdown_with_mermaid_on_demand(screen: Screen):
    ui.button('Create Mermaid', on_click=lambda: ui.markdown('''
        ```mermaid
        graph TD;
            Node_A --> Node_B;
        ```
    ''', extras=['mermaid', 'fenced-code-blocks']))

    screen.open('/')
    screen.click('Create Mermaid')
    assert screen.selenium.find_element(By.XPATH, '//span[p[contains(text(), "Node_A")]]').is_displayed()
    assert screen.selenium.find_element(By.XPATH, '//span[p[contains(text(), "Node_B")]]').is_displayed()


def test_strip_indentation(screen: Screen):
    ui.markdown('''
        **This is Markdown.**
    ''')

    screen.open('/')
    screen.should_contain('This is Markdown.')
    screen.should_not_contain('**This is Markdown.**')  # NOTE: '**' are translated to formatting and not visible


def test_replace_markdown(screen: Screen):
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
