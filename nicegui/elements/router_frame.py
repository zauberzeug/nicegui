from typing import Union, Callable, Tuple, Any, Optional, Self

from nicegui import ui, helpers, context, background_tasks, core
from nicegui.single_page_target import SinglePageTarget


class RouterFrame(ui.element, component='router_frame.js'):
    """The RouterFrame is a special element which is used by the SinglePageRouter to exchange the content of
    the current page with the content of the new page. It serves as container and overrides the browser's history
    management to prevent the browser from reloading the whole page."""

    def __init__(self,
                 base_path: str = "",
                 valid_path_masks: Optional[list[str]] = None,
                 use_browser_history: bool = True,
                 change_title: bool = False,
                 parent_router_frame: "RouterFrame" = None):
        """
        :param base_path: The base url path of this router frame
        :param valid_path_masks: A list of valid path masks which shall be allowed to be opened by the router
        :param use_browser_history: Optional flag to enable or disable the browser history management. Default is True.
        :param change_title: Optional flag to enable or disable the title change. Default is False.
        """
        super().__init__()
        self._props['valid_path_masks'] = valid_path_masks if valid_path_masks is not None else []
        self._props['browser_history'] = use_browser_history
        self.child_frames: dict[str, "RouterFrame"] = {}
        self.use_browser_history = use_browser_history
        self.change_title = change_title
        self.parent_frame = parent_router_frame
        if parent_router_frame is not None:
            parent_router_frame._register_sub_frame(valid_path_masks[0], self)
        self._on_resolve: Optional[Callable[[Any], SinglePageTarget]] = None
        self.on('open', lambda e: self.navigate_to(e.args))

    def on_resolve(self, on_resolve: Callable[[Any], SinglePageTarget]) -> Self:
        """Set the on_resolve function which is used to resolve the target to a SinglePageUrl
        :param on_resolve: The on_resolve function which receives a target object such as an URL or Callable and
            returns a SinglePageUrl object."""
        self._on_resolve = on_resolve
        return self

    def resolve_target(self, target: Any) -> SinglePageTarget:
        if self._on_resolve is not None:
            return self._on_resolve(target)
        raise NotImplementedError

    def navigate_to(self, target: Any, _server_side=False) -> None:
        """Open a new page in the browser by exchanging the content of the router frame
        :param target: the target route or builder function. If a list is passed, the second element is a boolean
            indicating whether the navigation should be server side only and not update the browser.
        :param _server_side: Optional flag which defines if the call is originated on the server side and thus
            the browser history should be updated. Default is False."""
        # check if sub router is active and might handle the target
        for path_mask, frame in self.child_frames.items():
            if path_mask == target or target.startswith(path_mask + "/"):
                frame.navigate_to(target, _server_side)
                return
        target_url = self.resolve_target(target)
        entry = target_url.entry
        if entry is None:
            if target_url.fragment is not None:
                ui.run_javascript(f'window.location.href = "#{target_url.fragment}";')  # go to fragment
                return
            return
        if self.change_title:
            title = entry.title if entry.title is not None else core.app.config.title
            ui.page_title(title)
        if _server_side and self.use_browser_history:
            ui.run_javascript(f'window.history.pushState({{page: "{target}"}}, "", "{target}");')

        async def build(content_element, fragment, kwargs) -> None:
            with content_element:
                result = entry.builder(**kwargs)
                if helpers.is_coroutine_function(entry.builder):
                    await result
                if fragment is not None:
                    await ui.run_javascript(f'window.location.href = "#{fragment}";')

        self.clear()
        combined_dict = {**target_url.path_args, **target_url.query_args}
        background_tasks.create(build(self, target_url.fragment, combined_dict))

    def clear(self) -> None:
        self.child_frames.clear()
        super().clear()

    def _register_sub_frame(self, path: str, frame: "RouterFrame") -> None:
        """Registers a sub frame to the router frame

        :param path: The path of the sub frame
        :param frame: The sub frame"""
        self.child_frames[path] = frame
