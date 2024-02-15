from typing import Callable, Dict, Union

from nicegui import background_tasks, helpers, ui


class RouterFrame(ui.element, component='router_frame.js'):
    """
    Represents a frame that acts as a router in a single-page application.

    This class is used to define a frame that can handle routing in a single-page application.
    It inherits from the `ui.element` class and uses the `router_frame.js` component.

    Usage:
        router_frame = RouterFrame()

    Attributes:
        - component (str): The name of the JavaScript component associated with this frame.

    Example:
        router_frame = RouterFrame()
    """
    pass

class Router():
    """
    A class that represents a router for a single-page application.

    The Router class is responsible for managing routes and rendering content based on the current route.

    Attributes:
        routes (Dict[str, Callable]): A dictionary that maps paths to builder functions.
        content (ui.element): The content element where the rendered content will be displayed.

    Methods:
        add(path: str) -> Callable: A decorator method used to add a route to the router.
        open(target: Union[Callable, str]) -> None: Opens the specified route or builder function.
        frame() -> ui.element: Returns the content element as a frame for the router.

    Example:
        router = Router()

        @router.add('/')
        def home():
            ui.html('<h1>Welcome to the Home Page!</h1>')

        @router.add('/about')
        def about():
            ui.html('<h1>About Us</h1><p>We are a team of developers.</p>')

        content_frame = router.frame()
        ui.render(content_frame)
    """

    def __init__(self) -> None:
        self.routes: Dict[str, Callable] = {}
        self.content: ui.element = None

    def add(self, path: str):
        """
        Decorator method used to add a route to the router.

        Args:
            path (str): The path of the route.

        Returns:
            Callable: The decorator function.

        Example:
            @router.add('/contact')
            def contact():
                ui.html('<h1>Contact Us</h1><p>Get in touch with us.</p>')
        """
        def decorator(func: Callable):
            self.routes[path] = func
            return func
        return decorator

    def open(self, target: Union[Callable, str]) -> None:
        """
        Opens the specified route or builder function.

        Args:
            target (Union[Callable, str]): The target route or builder function.

        Returns:
            None

        Example:
            router.open('/about')
        """
        if isinstance(target, str):
            path = target
            builder = self.routes[target]
        else:
            path = {v: k for k, v in self.routes.items()}[target]
            builder = target

        async def build() -> None:
            with self.content:
                ui.run_javascript(f'''
                    if (window.location.pathname !== "{path}") {{
                        history.pushState({{page: "{path}"}}, "", "{path}");
                    }}
                ''')
                result = builder()
                if helpers.is_coroutine_function(builder):
                    await result
        self.content.clear()
        background_tasks.create(build())

    def frame(self) -> ui.element:
        """
        Returns the content element as a frame for the router.

        Returns:
            ui.element: The content element.

        Example:
            content_frame = router.frame()
            ui.render(content_frame)
        """
        self.content = RouterFrame().on('open', lambda e: self.open(e.args))
        return self.content
