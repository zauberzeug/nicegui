from nicegui import ui
from nicegui.testing import Screen


def test_server_set_value_includes_value_in_update(screen: Screen):
    @ui.page('/')
    def page():
        inp = ui.input(value='initial')
        # Server-side change: flag should be False
        inp.value = 'from_server'
        assert inp._value_from_client is False
        # _to_dict always includes VALUE_PROP
        d = inp._to_dict()
        assert 'props' in d
        assert inp.VALUE_PROP in d['props']
        assert d['props'][inp.VALUE_PROP] == 'from_server'
        ui.label('server_test_passed')

    screen.open('/')
    screen.should_contain('server_test_passed')


def test_flag_set_true_when_simulating_client_change(screen: Screen):
    @ui.page('/')
    def page():
        inp = ui.input(value='initial')
        inp._value_from_client = True
        d = inp._to_dict()
        assert inp.VALUE_PROP in d['props']
        ui.label('flag_test_passed')

    screen.open('/')
    screen.should_contain('flag_test_passed')


def test_to_dict_always_includes_value(screen: Screen):
    @ui.page('/')
    def page():
        inp = ui.input(value='hello')
        inp._value_from_client = True
        d = inp._to_dict()
        assert inp.VALUE_PROP in d['props']
        assert d['props'][inp.VALUE_PROP] == 'hello'
        ui.label('reconnect_safe_passed')

    screen.open('/')
    screen.should_contain('reconnect_safe_passed')


def test_flag_false_by_default(screen: Screen):
    @ui.page('/')
    def page():
        inp = ui.input(value='test')
        assert inp._value_from_client is False
        select = ui.select(options=['a', 'b'], value='a')
        assert select._value_from_client is False
        ui.label('default_flag_passed')

    screen.open('/')
    screen.should_contain('default_flag_passed')


def test_loopback_true_server_change_keeps_flag_false(screen: Screen):
    @ui.page('/')
    def page():
        select = ui.select(options=['a', 'b', 'c'], value='a')
        assert select.LOOPBACK is True
        select.value = 'b'
        assert select._value_from_client is False
        ui.label('loopback_test_passed')

    screen.open('/')
    screen.should_contain('loopback_test_passed')
