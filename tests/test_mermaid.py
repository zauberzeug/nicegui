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
