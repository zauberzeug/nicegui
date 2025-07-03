from typing import Callable, Optional, Union

from nicegui import helpers, json, ui

from .code_extraction import get_full_code
from .intersection_observer import IntersectionObserver as intersection_observer
from .windows import browser_window, python_window


def demo(f: Callable, *, lazy: bool = True, tab: Optional[Union[str, Callable]] = None) -> Callable:
    """Render a callable as a demo with Python code and browser window."""
    with ui.column().classes('w-full items-stretch gap-8 no-wrap min-[1500px]:flex-row'):
        full_code = get_full_code(f)
        with python_window(classes='w-full max-w-[44rem]'):
            ui.markdown(f'````python\n{full_code}\n````')
            ui.icon('content_copy', size='xs') \
                .classes('absolute right-2 top-10 opacity-10 hover:opacity-80 cursor-pointer') \
                .on('click', js_handler=f'() => navigator.clipboard.writeText({json.dumps(full_code)})') \
                .on('click', lambda: ui.notify('Copied to clipboard', type='positive', color='primary'), [])
        with browser_window(title=tab,
                            classes='w-full max-w-[44rem] min-[1500px]:max-w-[20rem] min-h-[10rem] browser-window') as window:
            if lazy:
                spinner = ui.image('/static/loading.gif').classes('w-8 h-8').props('no-spinner no-transition')

                async def handle_intersection():
                    window.remove(spinner)
                    if helpers.is_coroutine_function(f):
                        await f()
                    else:
                        f()
                intersection_observer(on_intersection=handle_intersection)
            else:
                assert not helpers.is_coroutine_function(f), 'async functions are not supported in non-lazy demos'
                f()

    return f
