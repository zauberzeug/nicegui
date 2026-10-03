import pytest
from selenium.webdriver.common.by import By

from nicegui import events, ui
from nicegui.elements.mermaid.mermaid import _extract_node_id
from nicegui.testing import Screen


def test_mermaid(screen: Screen):
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

    screen.open('/')
    node_a = screen.selenium.find_element(By.XPATH, '//span[p[contains(text(), "Node_A")]]')
    assert node_a.get_attribute('class') == 'nodeLabel'

    screen.click('Set new content')
    node_c = screen.selenium.find_element(By.XPATH, '//span[p[contains(text(), "Node_C")]]')
    assert node_c.get_attribute('class') == 'nodeLabel'
    screen.should_not_contain('Node_A')


def test_mermaid_with_line_breaks(screen: Screen):
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

    screen.open('/')
    screen.should_contain('<<Requirement>>')
    screen.should_contain('ID: 1')
    screen.should_contain('Text: some test text')
    screen.should_contain('Risk: High')
    screen.should_contain('Verification: Test')


def test_mermaid_with_yaml_frontmatter(screen: Screen):
    @ui.page('/')
    def page():
        ui.mermaid('''
            ---
            displayMode: compact
            ---
            gantt
                title A Gantt Diagram
                dateFormat YYYY-MM-DD
                section Section
                    A task          :a1, 2014-01-01, 30d
                    Another task    :after a1, 20d
        ''')

    screen.open('/')
    screen.should_contain('A Gantt Diagram')
    screen.should_not_contain('Syntax error in text')


def test_replace_mermaid(screen: Screen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.mermaid('graph LR; Node_A')

        def replace():
            with container.clear():
                ui.mermaid('graph LR; Node_B')
        ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('Node_A')

    screen.click('Replace')
    screen.wait(0.5)
    screen.should_contain('Node_B')
    screen.should_not_contain('Node_A')


def test_create_dynamically(screen: Screen):
    @ui.page('/')
    def page():
        ui.button('Create', on_click=lambda: ui.mermaid('graph LR; Node'))

    screen.open('/')
    screen.click('Create')
    screen.should_contain('Node')


def test_error(screen: Screen):
    @ui.page('/')
    def page():
        ui.mermaid('''
            graph LR;
                A --> B;
                A -> C;
        ''').on('error', lambda e: ui.label(e.args['message']))

    screen.allowed_js_errors.append(':18 Object')
    screen.open('/')
    screen.should_contain('Syntax error in text')
    screen.should_contain('Parse error on line 3')


def test_error_source_accurate(screen: Screen):
    errors: list[events.GenericEventArguments] = []

    @ui.page('/')
    def page():
        ui.mermaid('graph TD; A --> B').on('error', errors.append)
        ui.mermaid('BAD SYNTAX')

    screen.allowed_js_errors.append(':18 Object')
    screen.open('/')
    assert not errors, 'No errors should be collected because the invalid diagram has no error handler'


@pytest.mark.parametrize('security_level', ['loose', 'strict'])
def test_click_mermaid_node(security_level: str, screen: Screen):
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

    screen.open('/')
    screen.click('Y')
    screen.wait(0.5)
    screen.should_not_contain('Clicked X')
    screen.should_not_contain('Clicked Z')
    if security_level == 'loose':
        screen.should_contain('Clicked Y')
    else:
        screen.should_not_contain('Clicked Y')


def test_node_click_handler(screen: Screen):
    @ui.page('/')
    def page():
        ui.mermaid('''
            flowchart TD;
                A[Node A];
                B[Node B];
                Node-With-Hyphen[Node With Hyphen];
        ''', on_node_click=lambda e: ui.notify(f'clicked [{e.node_id}]'))

    screen.open('/')
    screen.click('Node A')
    screen.should_contain('clicked [A]')  # the brackets keep a partially stripped ID like "flowchart-A" from matching

    screen.click('Node B')
    screen.should_contain('clicked [B]')

    screen.click('Node With Hyphen')
    screen.should_contain('clicked [Node-With-Hyphen]')  # make sure our ID extraction works even with hyphens


@pytest.mark.parametrize(('svg_id', 'html_id', 'node_id'), [
    ('c4_mermaid', 'c4_mermaid-flowchart-A-0', 'A'),
    ('c4_mermaid', 'c4_mermaid-flowchart-Node-With-Hyphen-1', 'Node-With-Hyphen'),
    ('c7_mermaid', 'c7_mermaid-state-s1-0', 's1'),
    ('c8_mermaid', 'c8_mermaid-classId-Animal-0', 'Animal'),
    ('c9_mermaid', 'c9_mermaid-entity-CUSTOMER-ORDER-0', 'CUSTOMER-ORDER'),
    ('c13_mermaid', 'c13_mermaid-A', 'A'),  # block, mindmap and requirement: no type token, no index
    ('c10_mermaid', 'c10_mermaid-node_0', 'node_0'),
    ('c11_mermaid', 'c11_mermaid-test_req', 'test_req'),
    ('c4_mermaid', 'c4_mermaid-flowchart-A-123-0', 'A-123'),  # a node ID may end in digits: the index is still last
    ('c13_mermaid', 'c13_mermaid-A-B-123', 'B'),  # known limit: indistinguishable from <type>-<node_id>-<index>
    # an unknown prefix must yield the raw ID, never a positional guess that recreates the old bug
    ('c4_mermaid', 'custom_mermaid-flowchart-A-0', 'custom_mermaid-flowchart-A-0'),
])
def test_extract_node_id(svg_id: str, html_id: str, node_id: str):
    assert _extract_node_id(html_id, svg_id) == node_id


@pytest.mark.parametrize(('content', 'label', 'node_id'), [
    ('classDiagram\n class Animal', 'Animal', 'Animal'),  # type token is "classId", not "flowchart"
    ('stateDiagram-v2\n s1 --> s2', 's1', 's1'),
    ('erDiagram\n CUSTOMER-ORDER ||--o{ LINE-ITEM : has', 'CUSTOMER-ORDER', 'CUSTOMER-ORDER'),
    # block, mindmap and requirement diagrams emit "<svg_id>-<node_id>": no type token, no index.
    # Only block is exercised here because Selenium cannot click the other two's SVG labels.
    ('block-beta\n columns 1\n A', 'A', 'A'),
])
def test_node_click_handler_with_other_diagram_types(screen: Screen, content: str, label: str, node_id: str):
    @ui.page('/')
    def page():
        ui.mermaid(content, on_node_click=lambda e: ui.notify(f'clicked [{e.node_id}]'))

    screen.open('/')
    screen.click(label)
    screen.should_contain(f'clicked [{node_id}]')
