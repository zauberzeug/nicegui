import inspect
import justpy as jp
from typing import Callable, Optional
from pygments.formatters import HtmlFormatter
from ..globals import config, page_stack, view_stack
from starlette.requests import Request

class Page(jp.QuasarPage):

    def __init__(self,
                 route: str,
                 title: Optional[str] = None,
                 favicon: Optional[str] = None,
                 dark: Optional[bool] = ...,
                 classes: str = 'q-ma-md column items-start',
                 css: str = HtmlFormatter().get_style_defs('.codehilite'),
                 on_connect: Optional[Callable] = None,
                 ):
        """Page

        Creates a new page at the given path.

        :param route: route of the new page (path must start with '/')
        :param title: optional page title
        :param favicon: optional favicon
        :param dark: whether to use Quasar's dark mode (defaults to `dark` argument of `run` command)
        :param classes: tailwind classes for the container div (default: `'q-ma-md column items-start'`)
        :param css: CSS definitions
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
        jp.Route(route, self.access)

    async def access(self, request: Request):
        if self.on_connect:
            argcount = len(inspect.getargspec(self.on_connect)[0])
            if argcount == 1:
                if inspect.iscoroutinefunction(self.on_connect):
                    await self.on_connect(request)
                else:
                    self.on_connect(request)
            elif argcount == 0:
                if inspect.iscoroutinefunction(self.on_connect):
                    await self.on_connect()
                else:
                    self.on_connect()
            else:
                raise ValueError(f'invalid number of arguments (0 or 1 allowed, got {argcount})')
        return self

    def __enter__(self):
        page_stack.append(self)
        view_stack.append(self.view)
        return self

    def __exit__(self, *_):
        page_stack.pop()
        view_stack.pop()
