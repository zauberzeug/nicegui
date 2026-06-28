from nicegui import ui
from nicegui.defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults


def test_default_props():
    @ui.page('/')
    def page():
        assert ui.button().props['color'] == 'primary', 'primary is the default color'

        ui.button.default_props('color=red')

        assert ui.button().props['color'] == 'red', 'if no color is passed, the default prop is used'
        assert ui.button(color=DEFAULT_PROP | 'primary').props['color'] == 'red', 'explicit sentinel uses defaults'
        assert ui.button(color='blue').props['color'] == 'blue', 'if a color is passed, it overrides the default prop'
        assert ui.button(color='primary').props['color'] == 'primary', 'even the default overrides the default prop'


def test_explicit_default_sentinels_are_resolved():
    class DummyElement:
        def __init__(self):
            self._default_props = {
                'value': 'value from defaults',
                'model-value': 'model value from defaults',
            }

        @resolve_defaults
        def method(self, value=DEFAULT_PROP | 'fallback', *,
                   model_value=DEFAULT_PROPS['model-value'] | 'model fallback'):
            return value, model_value

    element = DummyElement()

    assert element.method() == ('value from defaults', 'model value from defaults')
    assert element.method(value=DEFAULT_PROP | 'explicit fallback') == (
        'value from defaults', 'model value from defaults')
    assert element.method(model_value=DEFAULT_PROPS['custom-key'] | 'explicit fallback') == (
        'value from defaults', 'explicit fallback')
    assert element.method(DEFAULT_PROP | 'explicit fallback') == (
        'value from defaults', 'model value from defaults')


def test_positional_only_default_sentinels_are_resolved():
    class DummyElement:
        def __init__(self):
            self._default_props = {'value': 'value from defaults'}

        @resolve_defaults
        def method(self, value=DEFAULT_PROP | 'fallback', /):
            return value

    element = DummyElement()

    assert element.method() == 'value from defaults'
    assert element.method(DEFAULT_PROP | 'explicit fallback') == 'value from defaults'
