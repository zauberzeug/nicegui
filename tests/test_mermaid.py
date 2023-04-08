from nicegui import ui

from .screen import Screen


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
