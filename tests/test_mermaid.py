import pytest
from selenium.webdriver.common.by import By

from nicegui import events, ui
from nicegui.testing import SharedScreen


def test_mermaid(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        m = ui.mermaid('''
            graph TD;
                Node_A --> Node_B;
        ''')
        ui.button('Set new content', on_click=lambda: m.set_content('''
            graph TD;
                Node_C --> Node_D;
        '''))

    shared_screen.open('/')
    node_a = shared_screen.selenium.find_element(By.XPATH, '//span[p[contains(text(), "Node_A")]]')
    assert node_a.get_attribute('class') == 'nodeLabel'

    shared_screen.click('Set new content')
    node_c = shared_screen.selenium.find_element(By.XPATH, '//span[p[contains(text(), "Node_C")]]')
    assert node_c.get_attribute('class') == 'nodeLabel'
    shared_screen.should_not_contain('Node_A')


def test_mermaid_with_line_breaks(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.mermaid('''
            requirementDiagram

            requirement test_req {
                id: 1
                text: some test text
                risk: high
                verifymethod: test
            }
        ''')

    shared_screen.open('/')
    shared_screen.should_contain('<<Requirement>>')
    shared_screen.should_contain('ID: 1')
    shared_screen.should_contain('Text: some test text')
    shared_screen.should_contain('Risk: High')
    shared_screen.should_contain('Verification: Test')


def test_replace_mermaid(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.mermaid('graph LR; Node_A')

        def replace():
            with container.clear():
                ui.mermaid('graph LR; Node_B')
        ui.button('Replace', on_click=replace)

    shared_screen.open('/')
    shared_screen.should_contain('Node_A')

    shared_screen.click('Replace')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Node_B')
    shared_screen.should_not_contain('Node_A')


def test_create_dynamically(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.button('Create', on_click=lambda: ui.mermaid('graph LR; Node'))

    shared_screen.open('/')
    shared_screen.click('Create')
    shared_screen.should_contain('Node')


def test_error(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.mermaid('''
            graph LR;
                A --> B;
                A -> C;
        ''').on('error', lambda e: ui.label(e.args['message']))

    shared_screen.allowed_js_errors.append(':18 Object')
    shared_screen.open('/')
    shared_screen.should_contain('Syntax error in text')
    shared_screen.should_contain('Parse error on line 3')


def test_error_source_accurate(shared_screen: SharedScreen):
    errors: list[events.GenericEventArguments] = []

    @ui.page('/')
    def page():
        ui.mermaid('graph TD; A --> B').on('error', errors.append)
        ui.mermaid('BAD SYNTAX')

    shared_screen.allowed_js_errors.append(':18 Object')
    shared_screen.open('/')
    assert not errors, 'No errors should be collected because the invalid diagram has no error handler'


@pytest.mark.parametrize('security_level', ['loose', 'strict'])
def test_click_mermaid_node(security_level: str, shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.mermaid('''
            flowchart TD;
                X;
                click X call document.write("Clicked X")
        ''', config={'securityLevel': security_level})

        ui.mermaid('''
            flowchart TD;
                Y;
                click Y call document.write("Clicked Y")
        ''', config={'securityLevel': security_level})

        ui.mermaid('''
            flowchart TD;
                Z;
                click Z call document.write("Clicked Z")
        ''', config={'securityLevel': security_level})

    shared_screen.open('/')
    shared_screen.click('Y')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Clicked X')
    shared_screen.should_not_contain('Clicked Z')
    if security_level == 'loose':
        shared_screen.should_contain('Clicked Y')
    else:
        shared_screen.should_not_contain('Clicked Y')


def test_node_click_handler(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.mermaid('''
            flowchart TD;
                A[Node A];
                B[Node B];
                Node-With-Hyphen[Node With Hyphen];
        ''', on_node_click=lambda e: ui.notify(f'{e.node_id} clicked'))

    shared_screen.open('/')
    shared_screen.click('Node A')
    shared_screen.should_contain('A clicked')

    shared_screen.click('Node B')
    shared_screen.should_contain('B clicked')

    shared_screen.click('Node With Hyphen')
    shared_screen.should_contain('Node-With-Hyphen clicked')  # make sure our ID extraction works even with hyphens
