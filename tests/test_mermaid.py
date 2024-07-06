import pytest

from nicegui import ui
from nicegui.testing import Screen


def test_mermaid(screen: Screen):
    m = ui.mermaid('''
        graph TD;
            Node_A --> Node_B;
    ''')

    screen.open('/')
    assert screen.find('Node_A').get_attribute('class') == 'nodeLabel'

    m.set_content('''
graph TD;
    Node_C --> Node_D;
''')
    assert screen.find('Node_C').get_attribute('class') == 'nodeLabel'
    screen.should_not_contain('Node_A')


def test_mermaid_with_line_breaks(screen: Screen):
    ui.mermaid('''
        requirementDiagram

        requirement test_req {
            id: 1
            text: some test text
            risk: high
            verifymethod: test
        }
    ''')

    screen.open('/')
    screen.should_contain('<<Requirement>>')
    screen.should_contain('Id: 1')
    screen.should_contain('Text: some test text')
    screen.should_contain('Risk: High')
    screen.should_contain('Verification: Test')


def test_replace_mermaid(screen: Screen):
    with ui.row() as container:
        ui.mermaid('graph LR; Node_A')

    def replace():
        container.clear()
        with container:
            ui.mermaid('graph LR; Node_B')
    ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('Node_A')
    screen.click('Replace')
    screen.wait(0.5)
    screen.should_contain('Node_B')
    screen.should_not_contain('Node_A')


def test_create_dynamically(screen: Screen):
    ui.button('Create', on_click=lambda: ui.mermaid('graph LR; Node'))

    screen.open('/')
    screen.click('Create')
    screen.should_contain('Node')


def test_error(screen: Screen):
    ui.mermaid('''
    graph LR;
        A --> B;
        A -> C;
    ''').on('error', lambda e: ui.label(e.args['message']))

    screen.open('/')
    screen.should_contain('Syntax error in text')
    screen.should_contain('Parse error on line 3')


@pytest.mark.parametrize('security_level', ['loose', 'strict'])
def test_click_mermaid_node(security_level: str, screen: Screen):
    ui.mermaid('''
        flowchart TD;
            A;
            click A call document.write("Success")
    ''', config={'securityLevel': security_level})

    screen.open('/')
    screen.click('A')
    screen.wait(0.5)
    if security_level == 'loose':
        screen.should_contain('Success')
    else:
        screen.should_not_contain('Success')
