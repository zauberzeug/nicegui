import inspect
import justpy as jp
from typing import Awaitable, Callable, Optional, Union
from pygments.formatters import HtmlFormatter
from starlette.requests import Request
from ..globals import config, page_stack, view_stack

class Page(jp.QuasarPage):

    def __init__(self,
                 route: str,
                 title: Optional[str] = None,
                 favicon: Optional[str] = None,
                 dark: Optional[bool] = ...,
                 classes: str = 'q-ma-md column items-start',
                 css: str = HtmlFormatter().get_style_defs('.codehilite'),
                 on_connect: Optional[Union[Awaitable, Callable]] = None,
                 ):
        """Page

        Creates a new page at the given path.

        :param route: route of the new page (path must start with '/')
        :param title: optional page title
        :param favicon: optional favicon
        :param dark: whether to use Quasar's dark mode (defaults to `dark` argument of `run` command)
        :param classes: tailwind classes for the container div (default: `'q-ma-md column items-start'`)
        :param css: CSS definitions
        :param on_connect: optional function or coroutine which is called for each new client connection
        """
        super().__init__()

        self.delete_flag = False
        self.title = title or config.title
        self.favicon = favicon or config.favicon
        self.dark = dark if dark is not ... else config.dark
        self.tailwind = True  # use Tailwind classes instead of Quasars
        self.css = css
        self.on_connect = on_connect or config.on_connect
        self.head_html += '''
            <script>
                confirm = () => { setTimeout(location.reload.bind(location), 100); return false; };
            </script>
        '''  # avoid confirmation dialog for reload

        self.view = jp.Div(a=self, classes=classes, style='row-gap: 1em')
        self.view.add_page(self)

        self.route = route
        jp.Route(route, self._route_function)

    async def _route_function(self, request: Request):
        if self.on_connect:
            arg_count = len(inspect.signature(self.on_connect).parameters)
            is_coro = inspect.iscoroutinefunction(self.on_connect)
            if arg_count == 1:
                await self.on_connect(request) if is_coro else self.on_connect(request)
            elif arg_count == 0:
                await self.on_connect() if is_coro else self.on_connect()
            else:
                raise ValueError(f'invalid number of arguments (0 or 1 allowed, got {arg_count})')
        return self

    def __enter__(self):
        page_stack.append(self)
        view_stack.append(self.view)
        return self

    def __exit__(self, *_):
        page_stack.pop()
        view_stack.pop()
