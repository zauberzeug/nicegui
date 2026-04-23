from nicegui import ui
from nicegui.testing import Screen


def test_add_action_basic_structure(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        n.add_action(lambda: None, text='Click me')

    screen.open('/')
    screen.should_contain('Test')
    actions = n._props['options']['actions']
    assert len(actions) == 1
    assert actions[0]['label'] == 'Click me'
    assert actions[0]['noDismiss'] is False
    assert 'icon' not in actions[0]
    assert ':handler' in actions[0]


def test_add_action_with_icon(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        n.add_action(lambda: None, text='With icon', icon='check')
        n.add_action(lambda: None, text='No icon')

    screen.open('/')
    actions = n._props['options']['actions']
    assert actions[0]['icon'] == 'check'
    assert 'icon' not in actions[1]


def test_add_action_no_dismiss(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        n.add_action(lambda: None, text='Dismiss', no_dismiss=False)
        n.add_action(lambda: None, text='Stay', no_dismiss=True)

    screen.open('/')
    actions = n._props['options']['actions']
    assert actions[0]['noDismiss'] is False
    assert actions[1]['noDismiss'] is True


def test_add_action_quasar_color(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        n.add_action(lambda: None, text='Primary', color='primary')

    screen.open('/')
    action = n._props['options']['actions'][0]
    assert action['color'] == 'primary'
    assert 'class' not in action or 'text-' not in action.get('class', '')
    assert 'style' not in action or 'color:' not in action.get('style', '')


def test_add_action_tailwind_color(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        n.add_action(lambda: None, text='Blue', color='blue-500')

    screen.open('/')
    action = n._props['options']['actions'][0]
    assert 'text-blue-500' in action.get('class', '')
    assert 'color' not in action or action.get('color') != 'blue-500'


def test_add_action_css_color(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        n.add_action(lambda: None, text='Custom', color='#ff0000')

    screen.open('/')
    action = n._props['options']['actions'][0]
    assert 'color: #ff0000;' in action.get('style', '')


def test_add_action_no_color(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        n.add_action(lambda: None, text='No color', color=None)

    screen.open('/')
    action = n._props['options']['actions'][0]
    assert 'color' not in action
    assert 'class' not in action
    assert 'style' not in action


def test_add_action_kwargs_do_not_overwrite_color(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        n.add_action(lambda: None, text='Test', color='blue-500', **{'class': 'my-class'})

    screen.open('/')
    action = n._props['options']['actions'][0]
    # color-derived class should be present even though kwargs had 'class'
    assert 'text-blue-500' in action.get('class', '')


def test_add_action_multiple_actions(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        n.add_action(lambda: None, text='Action 1')
        n.add_action(lambda: None, text='Action 2')
        n.add_action(lambda: None, text='Action 3')

    screen.open('/')
    actions = n._props['options']['actions']
    assert len(actions) == 3
    assert actions[0]['label'] == 'Action 1'
    assert actions[1]['label'] == 'Action 2'
    assert actions[2]['label'] == 'Action 3'


def test_add_action_returns_self(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        result = n.add_action(lambda: None, text='Test')
        assert result is n

    screen.open('/')
