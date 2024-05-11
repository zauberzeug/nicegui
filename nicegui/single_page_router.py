from typing import Callable, Any, Optional, Self, Dict, TYPE_CHECKING

from nicegui import ui
from nicegui.context import context
from nicegui.elements.router_frame import RouterFrame
from nicegui.single_page_target import SinglePageTarget

PATH_RESOLVING_MAX_RECURSION = 100

if TYPE_CHECKING:
    from nicegui.single_page_router_config import SinglePageRouterConfig


class SinglePageRouter:
    """The SinglePageRouter manages the SinglePage navigation and content updates for a SinglePageApp instance.

    When ever a new page is opened, the SinglePageRouter exchanges the content of the current page with the content
    of the new page. The SinglePageRouter also manages the browser history and title updates.

    Multiple SinglePageRouters can be nested to create complex SinglePageApps with multiple content areas.

    See @ui.outlet or SinglePageApp for more information."""

    def __init__(self,
                 config: 'SinglePageRouterConfig',
                 included_paths: Optional[list[str]] = None,
                 excluded_paths: Optional[list[str]] = None,
                 use_browser_history: bool = True,
                 change_title: bool = True,
                 parent_router: 'SinglePageRouter' = None,
                 target_url: Optional[str] = None,
                 user_data: Optional[Dict] = None
                 ):
        """
        :param config: The SinglePageRouter which controls this router frame
        :param included_paths: A list of valid path masks which shall be allowed to be opened by the router
        :param excluded_paths: A list of path masks which shall be excluded from the router
        :param use_browser_history: Optional flag to enable or disable the browser history management. Default is True.
        :param change_title: Optional flag to enable or disable the title change. Default is True.
        :param target_url: The initial url of the router frame
        :param user_data: Optional user data which is passed to the builder functions of the router frame
        """
        super().__init__()
        self.router_config = config
        if target_url is None:
            if parent_router is not None and parent_router.target_url is not None:
                target_url = parent_router.target_url
            else:
                target_url = self.router_config.base_path
        self.user_data = user_data
        self.child_frames: dict[str, "SinglePageRouter"] = {}
        self.use_browser_history = use_browser_history
        self.change_title = change_title
        self.parent_frame = parent_router
        if parent_router is not None:
            parent_router._register_sub_frame(included_paths[0], self)
        self.router_frame = RouterFrame(base_path=self.router_config.base_path,
                                        target_url=target_url,
                                        included_paths=included_paths,
                                        excluded_paths=excluded_paths,
                                        use_browser_history=use_browser_history,
                                        on_navigate=lambda url, history: self.navigate_to(url, history=history),
                                        user_data={'router': self})
        self._on_navigate: Optional[Callable[[str], Optional[str]]] = None
        self._on_resolve: Optional[Callable[[str], SinglePageTarget]] = None

    @property
    def target_url(self) -> str:
        """The current target url of the router frame

        :return: The target url of the router frame"""
        return self.router_frame.target_url

    def resolve_target(self, target: Any, user_data: Optional[Dict] = None) -> SinglePageTarget:
        """Resolves a URL or SPA target to a SinglePageUrl which contains details about the builder function to
        be called and the arguments to pass to the builder function.

        :param target: The target object such as a URL or Callable
        :param user_data: Optional user data which is passed to the resolver functions
        :return: The resolved SinglePageUrl object"""
        if isinstance(target, SinglePageTarget):
            return target
        target = self.router_config.resolve_target(target)
        if target.valid and target.router is None:
            target.router = self
        if target is None:
            raise NotImplementedError
        if target.router_path is not None:
            rp = target.router_path
            original_path = target.original_path
            if rp.on_open is not None:
                target = rp.on_open(target, **user_data)
                if target.original_path != original_path:
                    return self.resolve_target(target, user_data)
        return target

    def handle_navigate(self, target: str) -> Optional[str]:
        """
        Is called when there was a navigation event in the browser or by the navigate_to method.

        By default the original target is returned. The SinglePageRouter and the router config (the outlet) can
        manipulate the target before it is resolved. If the target is None, the navigation is suppressed.

        :param target: The target URL
        :return: The target URL or None if the navigation is suppressed
        """
        cur_config = self.router_config
        while cur_config is not None:
            if cur_config.on_navigate is not None:
                new_target = cur_config.on_navigate(target)
                if new_target is None or new_target != target:
                    return new_target
            cur_config = cur_config.parent_config
        return target

    def navigate_to(self, target: [SinglePageTarget, str], server_side=True, sync=False,
                    history: bool = True) -> None:
        """Open a new page in the browser by exchanging the content of the router frame

        :param target: The target page or url.
        :param server_side: Optional flag which defines if the call is originated on the server side and thus
            the browser history should be updated. Default is False.
        :param sync: Optional flag to define if the content should be updated synchronously. Default is False.
        :param history: Optional flag defining if the history setting shall be respected. Default is True.
        """
        # check if sub router is active and might handle the target
        for path_mask, frame in self.child_frames.items():
            if path_mask == target or target.startswith(path_mask + '/'):
                frame.navigate_to(target, server_side)
                return
        if isinstance(target, str):
            target = self.handle_navigate(target)
            if target is None:
                return
        recursive_user_data = SinglePageRouter.get_user_data() | self.user_data | self.router_frame.user_data
        target = self.resolve_target(target, user_data=recursive_user_data)
        if target is None or not target.valid:  # navigation suppressed
            return
        original_path = target.original_path
        if history and not server_side and self.use_browser_history:  # triggered by the browser
            ui.run_javascript(f'window.history.pushState({{page: "{original_path}"}}, "", "{original_path}");')
            print("X Navigating to ", original_path)
        if target.builder is None:
            if target.fragment is not None:
                ui.run_javascript(f'window.location.href = "#{target.fragment}";')  # go to fragment
                return
            target = SinglePageTarget(builder=self._page_not_found, title='Page not found')
        if server_side and self.use_browser_history and history:
            ui.run_javascript(
                f'window.history.pushState({{page: "{original_path}"}}, "", "{original_path}");')
            print("Y Navigating to ", original_path)
        self.router_frame.target_url = target.original_path
        builder_kwargs = {**target.path_args, **target.query_args, 'url_path': original_path}
        target_fragment = target.fragment
        builder_kwargs.update(recursive_user_data)
        self.router_frame.update_content(target.builder, builder_kwargs, target.title, target_fragment, sync)

    def clear(self) -> None:
        """Clear the content of the router frame and removes all references to sub frames"""
        self.child_frames.clear()
        self.router_frame.clear()

    def update_user_data(self, new_data: dict) -> None:
        """Update the user data of the router frame

        :param new_data: The new user data to set"""
        self.user_data.update(new_data)

    @staticmethod
    def get_user_data() -> Dict:
        """Returns a combined dictionary of all user data of the parent router frames"""
        result_dict = {}
        for slot in context.slot_stack:
            if isinstance(slot.parent, RouterFrame):
                result_dict.update(slot.parent.user_data['router'].user_data)
        return result_dict

    @staticmethod
    def get_current_frame() -> Optional["SinglePageRouter"]:
        """Get the current router frame from the context stack

        :return: The current router or None if no router in the context stack"""
        for slot in reversed(context.slot_stack):  # we need to inform the parent router frame about
            if isinstance(slot.parent, RouterFrame):  # our existence so it can navigate to our pages
                return slot.parent.user_data['router']
        return None

    def _register_sub_frame(self, path: str, frame: "SinglePageRouter") -> None:
        """Registers a sub frame to the router frame

        :param path: The path of the sub frame
        :param frame: The sub frame"""
        self.child_frames[path] = frame
        self.router_frame.child_frame_paths = list(self.child_frames.keys())

    @staticmethod
    def _page_not_found():
        """
        Default builder function for the page not found error page
        """
        ui.label(f'Oops! Page Not Found 🚧').classes('text-3xl')
        ui.label(f'Sorry, the page you are looking for could not be found. 😔')
