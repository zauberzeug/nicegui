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
    assert 'class' not in action
    assert 'style' not in action


def test_add_action_tailwind_color(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        n.add_action(lambda: None, text='Blue', color='blue-500')

    screen.open('/')
    action = n._props['options']['actions'][0]
    assert action['class'] == 'text-blue-500'
    assert 'color' not in action
    assert 'style' not in action


def test_add_action_css_color(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        n.add_action(lambda: None, text='Custom', color='#ff0000')

    screen.open('/')
    action = n._props['options']['actions'][0]
    assert action['style'] == 'color: #ff0000;'
    assert 'color' not in action
    assert 'class' not in action


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


def test_add_action_kwargs_override_color(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        n.add_action(lambda: None, text='Test', color='blue-500', **{'class': 'my-class'})

    screen.open('/')
    action = n._props['options']['actions'][0]
    # explicit kwargs win: user's class clobbers the color-derived class
    assert action['class'] == 'my-class'


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
    assert 'index: 0' in actions[0][':handler']
    assert 'index: 1' in actions[1][':handler']
    assert 'index: 2' in actions[2][':handler']


def test_add_action_returns_self(screen: Screen):
    n = None

    @ui.page('/')
    def page():
        nonlocal n
        n = ui.notification('Test', timeout=None)
        result = n.add_action(lambda: None, text='Test')
        assert result is n

    screen.open('/')


def test_add_action_on_click_fires(screen: Screen):
    clicked: list[str] = []

    @ui.page('/')
    def page():
        n = ui.notification('Decide', timeout=None)
        n.add_action(lambda: clicked.append('yes'), text='Yes')
        n.add_action(lambda: clicked.append('no'), text='No')

    screen.open('/')
    screen.click('No')  # click the second action to verify the index dispatch picks the right handler
    screen.wait(0.5)
    assert clicked == ['no']


def test_add_action_after_render_no_duplicate(screen: Screen):
    """Adding an action after the notification is on screen must not re-render and duplicate it (see PR #4819)."""
    clicked: list[str] = []

    @ui.page('/')
    def page():
        n = ui.notification('Decide', timeout=None)
        ui.button('Add', on_click=lambda: n.add_action(lambda: clicked.append('late'), text='Late'))

    screen.open('/')
    assert len(screen.find_all_by_class('q-notification')) == 1
    screen.click('Add')
    screen.wait(0.5)
    assert len(screen.find_all_by_class('q-notification')) == 1, 'late add_action must not duplicate the notification'
    screen.click('Late')
    screen.wait(0.5)
    assert clicked == ['late']
