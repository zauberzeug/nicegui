import pytest
from selenium.webdriver.common.by import By

from nicegui import events, ui
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
    screen.should_not_contain('Clicked X', duration=1.0)
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
                A-123[Node A-123];
        ''', on_node_click=lambda e: ui.notify(f'clicked [{e.node_id}]'))

    screen.open('/')
    screen.click('Node A')
    screen.should_contain('clicked [A]')  # the brackets keep a partially stripped ID like "flowchart-A" from matching

    screen.click('Node B')
    screen.should_contain('clicked [B]')

    screen.click('Node With Hyphen')
    screen.should_contain('clicked [Node-With-Hyphen]')  # make sure our ID extraction works even with hyphens

    screen.click('Node A-123')
    screen.should_contain('clicked [A-123]')  # a trailing number must not be mistaken for Mermaid's node index


def test_icon_ids_do_not_collide_with_element_ids(screen: Screen):
    @ui.page('/')
    def page():
        ui.mermaid('''
            architecture-beta
                service db(database)[Database]
                service cache(database)[Cache]
                service server(server)[Server]
                db:R -- L:server
                cache:T -- B:server
        ''')
        for i in range(30):
            ui.label(f'Label {i}')

    screen.open('/')
    screen.should_contain('Database')
    ids = screen.selenium.execute_script('return Array.from(document.querySelectorAll("[id]"), e => e.id)')
    assert len(ids) == len(set(ids)), 'every id on the page should be unique'


@pytest.mark.parametrize(('content', 'nodes', 'config'), [
    # the other diagram types that add a type token and an index ("<svg_id>-<type>-<node_id>-<index>")
    ('graph TD\n A-1', {'A-1': 'A-1'}, {'flowchart': {'defaultRenderer': 'dagre-d3'}}),  # legacy "flowchart" detector
    ('flowchart-elk TD\n A-1', {'A-1': 'A-1'}, None),
    ('classDiagram\n class Animal', {'Animal': 'Animal'}, None),  # type token is "classId", not "flowchart"
    ('classDiagram-v2\n class Animal', {'Animal': 'Animal'}, None),
    ('stateDiagram\n s1 --> s2', {'s1': 's1'}, None),
    ('stateDiagram-v2\n s1 --> s2', {'s1': 's1'}, None),
    ('erDiagram\n CUSTOMER-ORDER ||--o{ LINE-ITEM : has', {'CUSTOMER-ORDER': 'CUSTOMER-ORDER'}, None),
    # all other diagram types use the node ID verbatim ("<svg_id>-<node_id>")
    ('block-beta\n columns 1\n A', {'A': 'A'}, None),
    ('requirementDiagram\n requirement "A-B-123" {\n id: 1\n }\n requirement "A-B-124" {\n id: 2\n }',
     {'A-B-123': 'A-B-123', 'A-B-124': 'A-B-124'}, None),  # used to be truncated to "B" and to collide with each other
    ('kanban\n todo[Todo]\n  A-B-123[Task 1]\n  A-B-124[Task 2]', {'Task 1': 'A-B-123', 'Task 2': 'A-B-124'}, None),
    # mindmap generates its own node IDs
    ('mindmap\n root((Root))\n  Child', {'Root': 'node_0', 'Child': 'node_1'}, None),
])
def test_node_click_handler_with_other_diagram_types(screen: Screen,
                                                     content: str, nodes: dict[str, str], config: dict | None):
    @ui.page('/')
    def page():
        ui.mermaid(content, config, on_node_click=lambda e: ui.notify(f'clicked [{e.node_id}]'))

    screen.open('/')
    for label, node_id in nodes.items():
        screen.click(label)
        screen.should_contain(f'clicked [{node_id}]')
