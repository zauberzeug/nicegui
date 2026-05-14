from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen


def test_skip_link_focuses_target(screen: Screen):
    target = None

    @ui.page('/')
    def page():
        nonlocal target
        ui.button('Navigation 1')
        target = ui.label('Main content')
        ui.skip_link(target=target)

    screen.open('/')
    link = screen.find_by_class('nicegui-skip-link')
    assert link.get_attribute('textContent') == 'Skip to main content'
    assert link.get_attribute('href').endswith(f'#c{target.id}')

    screen.selenium.execute_script('arguments[0].focus(); arguments[0].click();', link)
    screen.wait_for(lambda: screen.selenium.switch_to.active_element.get_attribute('id') == f'c{target.id}')


def test_custom_text(screen: Screen):
    @ui.page('/')
    def page():
        target = ui.label('Main content')
        ui.skip_link('Skip navigation', target=target)

    screen.open('/')
    link = screen.find_by_class('nicegui-skip-link')
    assert link.get_attribute('textContent') == 'Skip navigation'


def test_context_manager_replaces_text(screen: Screen):
    @ui.page('/')
    def page():
        target = ui.label('Main content')
        with ui.skip_link(text='', target=target):
            ui.label('Jump to content')

    screen.open('/')
    link = screen.find_by_class('nicegui-skip-link')
    assert link.get_attribute('textContent') == 'Jump to content'


def test_link_precedes_other_content_in_document(screen: Screen):
    @ui.page('/')
    def page():
        ui.button('First button')
        with ui.column() as main:
            ui.label('Main content')
        ui.skip_link(target=main)

    screen.open('/')
    is_before = screen.selenium.execute_script('''
        const link = document.querySelector('.nicegui-skip-link');
        const button = [...document.querySelectorAll('button')]
            .find(b => b.textContent.includes('First button'));
        return !!(link.compareDocumentPosition(button) & Node.DOCUMENT_POSITION_FOLLOWING);
    ''')
    assert is_before


def test_multiple_skip_links_preserve_order_and_precede_content(screen: Screen):
    @ui.page('/')
    def page():
        ui.button('Navigation')
        a = ui.label('Section A')
        b = ui.label('Section B')
        ui.skip_link('First', target=a)
        ui.skip_link('Second', target=b)

    screen.open('/')
    links = screen.selenium.find_elements(By.CSS_SELECTOR, '.nicegui-skip-link')
    assert [link.get_attribute('textContent') for link in links] == ['First', 'Second']
    # both links must precede the regular content in document order
    both_before_button = screen.selenium.execute_script('''
        const links = [...document.querySelectorAll('.nicegui-skip-link')];
        const button = [...document.querySelectorAll('button')]
            .find(b => b.textContent.includes('Navigation'));
        return links.every(link =>
            !!(link.compareDocumentPosition(button) & Node.DOCUMENT_POSITION_FOLLOWING));
    ''')
    assert both_before_button
