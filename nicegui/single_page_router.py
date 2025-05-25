from __future__ import annotations

from fnmatch import fnmatch
from typing import TYPE_CHECKING, Awaitable, Callable, Dict, Optional, Self, Union

from nicegui import background_tasks, core, ui
from nicegui.builder_utils import run_safe
from nicegui.context import context
from nicegui.elements.frame import Frame
from nicegui.single_page_target import SinglePageTarget

if TYPE_CHECKING:
    from .content import Content
    from .single_page_router import SinglePageRouter

PATH_RESOLVING_MAX_RECURSION = 100


class SinglePageRouter:
    """The SinglePageRouter manages the SinglePage navigation and content updates for a SinglePageApp instance.

    When ever a new page is opened, the SinglePageRouter exchanges the content of the current page with the content
    of the new page. The SinglePageRouter also manages the browser history and title updates.

    See ui.content for more information."""

    def __init__(self,
                 *,
                 content: Content,
                 included_paths: Optional[list[str]] = None,
                 excluded_paths: Optional[list[str]] = None,
                 use_browser_history: bool = True,
                 change_title: bool = True,
                 parent: SinglePageRouter = None,
                 target_url: Optional[str] = None,
                 user_data: Optional[Dict] = None
                 ):
        """
        :param content: The Content which controls this router frame
        :param included_paths: A list of valid path masks which shall be allowed to be opened by the router
        :param excluded_paths: A list of path masks which shall be excluded from the router
        :param use_browser_history: Optional flag to enable or disable the browser history management. Default is True.
        :param change_title: Optional flag to enable or disable the title change. Default is True.
        :param target_url: The initial url of the router frame
        :param user_data: Optional user data which is passed to the builder functions of the router frame
        """
        super().__init__()
        self.router_config = content
        self.base_path = content.base_path
        if target_url is None:
            if parent is not None and parent.target_url is not None:
                target_url = parent.target_url
            else:
                target_url = self.router_config.base_path
        self.user_data = user_data if user_data is not None else {}
        self.child_routers: dict[str, SinglePageRouter] = {}
        self.use_browser_history = use_browser_history
        self.change_title = change_title
        self.parent = parent
        # split base path into it's elements
        base_path_elements = self.router_config.base_path.split('/')
        # replace all asterisks with the actual path elements from target url where possible
        target_url_elements = target_url.split('/')
        for i, element in enumerate(base_path_elements):
            if element.startswith('{') and element.endswith('}'):
                if i < len(target_url_elements):
                    base_path_elements[i] = target_url_elements[i]
        # repeat the same for all included paths
        if included_paths is not None:
            for i, path in enumerate(included_paths):
                path_elements = path.split('/')
                for j, element in enumerate(path_elements):
                    if element == '*':
                        if j < len(base_path_elements):
                            path_elements[j] = base_path_elements[j]
                included_paths[i] = '/'.join(path_elements)
        self.base_path = '/'.join(base_path_elements)
        if parent is not None:
            parent._register_child_router(self.base_path, self)

        self.included_paths = set()
        self.excluded_paths = set()
        if included_paths is not None:
            for path in included_paths:
                cleaned = path.rstrip('/')
                self.included_paths.add(cleaned)
                self.included_paths.add(cleaned + '/*')
        if excluded_paths is not None:
            for path in excluded_paths:
                cleaned = path.rstrip('/')
                self.excluded_paths.add(cleaned)
                self.excluded_paths.add(cleaned + '/*')

        if user_data is None:
            user_data = {}
        user_data['router'] = self
        self.frame = Frame(router=self,
                           base_path=self.base_path,
                           target_url=target_url,
                           included_paths=list(self.included_paths) if self.included_paths else None,
                           excluded_paths=list(self.excluded_paths) if self.excluded_paths else None,
                           use_browser_history=use_browser_history,
                           on_navigate=lambda url, history: self.navigate_to(url, history=history))
        self._on_navigate: Optional[Callable[[str], Optional[Union[SinglePageTarget, str]]]] = None
        self.views = {}

    def add_included_path(self, path: str):
        """Add a path to the included paths list"""
        cleaned = path.rstrip('/')
        self.included_paths.add(cleaned)
        self.included_paths.add(cleaned + '/*')
        self.frame._props['included_path_masks'] += [cleaned, cleaned + '/*']

    def add_view(self, path: str, builder: Callable, title: Optional[str] = None, **kwargs) -> Self:
        """Add a view to the router

        :param path: The path of the view
        :param builder: The builder function of the view
        :param title: The title of the view
        :param kwargs: Additional arguments"""
        path = path.lstrip('/')
        if path in self.views:
            raise ValueError(f'View with path {path} already exists')
        self.views[path] = RouterView(path, builder, title, **kwargs)
        absolute_path = (self.base_path.rstrip('/') + path).rstrip('/')
        self.add_included_path(absolute_path)
        return self

    @property
    def target_url(self) -> str:
        """The current target url of the router frame

        :return: The target url of the router frame"""
        return self.frame.target_url

    def resolve_url(self, target: str) -> SinglePageTarget:
        """Resolves a URL target to a SinglePageTarget which contains details about the builder function to
        be called and the arguments to pass to the builder function.

        :param target: The target object such as a URL or Callable
        :return: The resolved SinglePageTarget object"""
        target = self.router_config.resolve_target(target)
        assert target.path is not None
        if isinstance(target, SinglePageTarget) and not target.valid and target.path.startswith(self.base_path):
            rem_path = target.path[len(self.base_path):]
            if rem_path in self.views:
                target.builder = self.views[rem_path].builder
                target.title = self.views[rem_path].title
                target.valid = True
        if target.valid and target.router is None:
            target.router = self
        if target is None:
            raise NotImplementedError
        return target

    def handle_navigate(self, target: str) -> Union[SinglePageTarget, str, None]:
        """Is called when there was a navigation event in the browser or by the navigate_to method.

        By default, the original target is returned. The SinglePageRouter and the router config can
        manipulate the target before it is resolved. If the target is None, the navigation is suppressed.

        :param target: The target URL
        :return: The target URL, a completely resolved target or None if the navigation is suppressed"""
        if self._on_navigate is not None:
            custom_target = self._on_navigate(target)
            if custom_target is None:
                return None
            if isinstance(custom_target, SinglePageTarget):
                return custom_target
            target = custom_target
        new_target = self.router_config.handle_navigate(target)
        if isinstance(target, SinglePageTarget):
            return target
        if new_target is None or new_target != target:
            return new_target
        return target

    def navigate_to(self, target: Union[SinglePageTarget, str, None], server_side=True,
                    history: bool = True) -> Awaitable | None:
        """Open a new page in the browser by exchanging the content of the router frame

        :param target: The target page or path.
        :param server_side: Optional flag which defines if the call is originated on the server side and thus
            the browser history should be updated. Default is False.
        :param history: Optional flag defining if the history setting shall be respected. Default is True.
        :return: Builder coroutine if it is async
        """
        # check if sub router is active and might handle the target
        if isinstance(target, str):
            for path_mask, frame in self.child_routers.items():
                if fnmatch(target, path_mask) or fnmatch(target, path_mask.rstrip('/') + '/*'):
                    frame.navigate_to(target, server_side)
                    return
            target = self.handle_navigate(target)
            if target is None:
                return
        handler_kwargs = (SinglePageRouter.get_user_data() | self.user_data |
                          {'previous_url_path': self.frame.target_url})
        # add user data of parent frames
        parent = self.parent
        while parent is not None:
            handler_kwargs.update(parent.user_data)
            parent = parent.parent
        if target is None:
            # TODO in which cases can the target be None? What should be the behavior?
            raise ValueError('Target is None')
        handler_kwargs['url_path'] = target if isinstance(target, str) else target.original_path
        if not isinstance(target, SinglePageTarget):
            target = self.resolve_url(target)
        if target is None or not target.valid:  # navigation suppressed
            return
        target_url = target.original_path
        assert target_url is not None

        # Skip rebuilding if we're navigating to the same page with the same builder
        current_target = self.target
        if (current_target is not None and
            target_url == self.frame.target_url and
                target.builder == current_target.builder):
            return

        handler_kwargs['target_url'] = target_url
        self._update_target_url(target_url)
        js_code = ''
        if history and self.use_browser_history:  # triggered by the browser
            js_code += f'window.history.pushState({{page: "{target_url}"}}, "", "{target_url}");'
        if target.builder is None:
            if target.fragment is not None:
                js_code += f'window.location.href = "#{target.fragment}";'  # go to fragment
                ui.run_javascript(js_code)
                return
            target = SinglePageTarget(builder=self._page_not_found, title='Page not found')
        if len(js_code) > 0:
            ui.run_javascript(js_code)
        handler_kwargs = {**target.path_args, **target.query_args, 'target': target} | handler_kwargs
        return self.update_content(target, handler_kwargs=handler_kwargs)

    def update_content(self, target: SinglePageTarget, handler_kwargs: dict):
        """Update the content of the router frame"""
        if target.on_pre_update is not None:
            run_safe(target.on_pre_update, **handler_kwargs)
        self.clear()
        self.user_data['target'] = target

        async def build() -> None:
            with self.frame:
                result = run_safe(target.builder, **handler_kwargs)
                if result:
                    await result
                if target.fragment is not None:
                    await ui.run_javascript(f'window.location.href = "#{target.fragment}";')

        background_tasks.create(build())

        if self.change_title and target.builder and len(self.child_routers) == 0:
            # note: If the router is just a container for sub routers, the title is not updated here but
            # in the sub router's update_content method
            title = target.title if target.title is not None else core.app.config.title
            ui.page_title(title)
        if target.on_post_update is not None:
            run_safe(target.on_post_update, **handler_kwargs)

    def clear(self) -> None:
        """Clear the content of the router frame and removes all references to sub frames"""
        self.child_routers.clear()
        self.frame.clear()

    def update_user_data(self, new_data: dict) -> None:
        """Update the user data of the router frame

        :param new_data: The new user data to set"""
        self.user_data.update(new_data)

    def on_navigate(self, callback: Callable[[str], Optional[Union[SinglePageTarget, str]]]) -> Self:
        """Set the on navigate callback which is called when a navigation event is triggered

        :param callback: The callback function"""
        self._on_navigate = callback
        return self

    @staticmethod
    def get_user_data() -> Dict:
        """Returns a combined dictionary of all user data of the parent router frames"""
        result_dict = {}
        for slot in context.slot_stack:
            if isinstance(slot.parent, Frame):
                result_dict.update(slot.parent.router.user_data)
        return result_dict

    @property
    def target(self) -> Optional[SinglePageTarget]:
        """The current target of the router frame. Only valid while a view is being built."""
        return self.user_data.get('target', None)

    @staticmethod
    def current_frame() -> Optional[SinglePageRouter]:
        """Get the current router frame from the context stack

        :return: The current router or None if no router in the context stack"""
        for slot in reversed(context.slot_stack):  # we need to inform the parent router frame about
            if isinstance(slot.parent, Frame):  # our existence so it can navigate to our pages
                return slot.parent.router
        return None

    def _register_child_router(self, path: str, frame: SinglePageRouter) -> None:
        """Registers a child router which handles a certain sub path

        :param path: The path of the child router
        :param frame: The child router"""
        self.child_routers[path] = frame
        # Update the frame's child_frame_paths property to trigger the setter
        paths = list(self.child_routers.keys())
        self.frame.child_frame_paths = paths

    @staticmethod
    def _page_not_found() -> None:
        """Default builder function for the page not found error page"""
        ui.label('Oops! Page Not Found 🚧').classes('text-3xl')
        ui.label('Sorry, the page you are looking for could not be found. 😔')

    def is_path_excluded(self, path: str) -> bool:
        """Check if a path matches any excluded paths.

        :param path: The path to check
        :return: True if the path matches any excluded paths, False otherwise"""
        for excluded_path in self.excluded_paths:
            # Convert excluded path to regex pattern like frame.js does
            pattern = '^' + excluded_path.replace('*', '.*') + '$'
            if excluded_path.endswith('/*'):
                pattern = '^' + excluded_path[:-2] + '(/.*)?$'
            if __import__('re').match(pattern, path):
                return True
        return False

    def is_path_included(self, path: str) -> bool:
        """Check if a path is included in this router.
        A path is included if it matches an included path and doesn't match any excluded paths.

        :param path: The path to check
        :return: True if the path is included, False otherwise"""
        if self.is_path_excluded(path):
            return False
        for included_path in self.included_paths:
            # Convert included path to regex pattern like frame.js does
            pattern = '^' + included_path.replace('*', '.*') + '$'
            if included_path.endswith('/*'):
                pattern = '^' + included_path[:-2] + '(/.*)?$'
            if __import__('re').match(pattern, path):
                return True
        return False

    def _update_target_url(self, target_url: str) -> None:
        """Updates the target url of the router and all parent routers

        :param target_url: The new target url"""
        cur_router = self
        for _ in range(PATH_RESOLVING_MAX_RECURSION):
            cur_router.frame.target_url = target_url
            cur_router = cur_router.parent
            if cur_router is None:
                return


class RouterView:
    """Defines a single, router instance specific view / "content page" which is displayed"""

    def __init__(self, path: str, builder: Callable, title: Optional[str] = None, **kwargs):
        self.path = path
        self.builder = builder
        self.title = title
        self.kwargs = kwargs

    def build_page(self, **kwargs):
        """Build the page content"""
        self.builder(**kwargs)
