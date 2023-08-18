"""React Style Reactive Component for NiceGUI.

It enables us to write code like this:
```python
from nicegui import ui

@reactive
def comp():
    count, set_count = use_state(0)
    ui.label('Count: ' + str(count))
    ui.button('Increment').on('click', lambda: set_count(count + 1))
```
"""
import sys
from typing import Callable

from nicegui import ui
from nicegui.helpers import is_coroutine_function


def use_state(default: any):
    """Should ONLY be used in a function that is decorated by `@reactive`, and should never call this conditionally.
    The lifecycle of the state is the same as the component rendered in the page.
    Internally the state is tied to the result of a component call.
    This means in the following example, `a` and `b` will have different states and all operations on `a` will see the same state.
    ```python
    @reactive
    def comp():
        count, set_count = use_state(0)
        ui.label('Count: ' + str(count))
        ui.button('Increment').on('click', lambda: set_count(count + 1))

    a = comp()
    b = comp()
    ```
    """
    frame = sys._getframe()
    while not '_context_state_' in frame.f_locals:
        frame = frame.f_back
    state = frame.f_locals['_context_state_']
    refreshable_func = state.get('_refreshable_func')

    key = state['__idx']
    value = state.setdefault(key, default)
    state['__idx'] += 1

    def set_value(value):
        state.update({key: value})
        refreshable_func.refresh()
    return value, set_value


def use_thread(fn):
    """Trigger a task on component mounted, ONLY ONCE during the lifetime of the component.

    This is useful when you want to trigger a task on component mounted, and you don't want to trigger it again when the component is refreshed.
    Typically used when you want to show a skeleton when the component is mounted, and then fetch data and render the real content.
    """
    runned, set_runned = ui.use_state(False)
    if not runned:
        set_runned(True)
        return ui.timer(0, fn, once=True)


def reactive(func: Callable):
    """Reactive Component Decorator for NiceGUI.

    Use `ui.reactive` to decorate a function.
    Then you can use `use_state` to create a state variable and manage state in a React way.
    """
    def __refresh_wrapper__(*args, **kwargs):
        def _co():
            _context_state_ = {}
            if not is_coroutine_function(func):
                def __state_wrapper__(*args, **kwargs):
                    nonlocal _context_state_
                    _context_state_['__idx'] = 0
                    return func(*args, **kwargs)
                return __state_wrapper__, _context_state_
            else:
                async def __state_wrapper__(*args, **kwargs):
                    nonlocal _context_state_
                    _context_state_['__idx'] = 0
                    return await func(*args, **kwargs)
                return __state_wrapper__, _context_state_

        f, state = _co()
        _refreshable_func = ui.refreshable(f)
        state['_refreshable_func'] = _refreshable_func
        return _refreshable_func(*args, **kwargs)
    return __refresh_wrapper__
