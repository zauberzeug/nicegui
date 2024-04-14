from typing import Union, Callable, Tuple, Any, Optional, Self

from nicegui import ui, helpers, context, background_tasks, core
from nicegui.router_frame_url import SinglePageUrl


class RouterFrame(ui.element, component='router_frame.js'):
    """The RouterFrame is a special element which is used by the SinglePageRouter to exchange the content of
    the current page with the content of the new page. It serves as container and overrides the browser's history
    management to prevent the browser from reloading the whole page."""

    def __init__(self, valid_path_masks: list[str],
                 use_browser_history: bool = True,
                 change_title: bool = False):
        """
        :param valid_path_masks: A list of valid path masks which shall be allowed to be opened by the router
        :param use_browser_history: Optional flag to enable or disable the browser history management. Default is True.
        :param change_title: Optional flag to enable or disable the title change. Default is False.
        """
        super().__init__()
        self._props['valid_path_masks'] = valid_path_masks
        self._props['browser_history'] = use_browser_history
        self.use_browser_history = use_browser_history
        self.change_title = False
        self._on_resolve: Optional[Callable[[Any], SinglePageUrl]] = None
        self.on('open', lambda e: self.navigate_to(e.args))

    def on_resolve(self, on_resolve: Callable[[Any], SinglePageUrl]) -> Self:
        """Set the on_resolve function which is used to resolve the target to a SinglePageUrl
        :param on_resolve: The on_resolve function which receives a target object such as an URL or Callable and
            returns a SinglePageUrl object."""
        self._on_resolve = on_resolve
        return self

    def get_target_url(self, target: Any) -> SinglePageUrl:
        if self._on_resolve is not None:
            return self._on_resolve(target)
        raise NotImplementedError

    def navigate_to(self, target: Any, _server_side=False) -> None:
        """Open a new page in the browser by exchanging the content of the router frame
        :param target: the target route or builder function. If a list is passed, the second element is a boolean
            indicating whether the navigation should be server side only and not update the browser.
        :param _server_side: Optional flag which defines if the call is originated on the server side and thus
            the browser history should be updated. Default is False."""
        target_url = self.get_target_url(target)
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

        content = context.get_client().single_page_content
        content.clear()
        combined_dict = {**target_url.path_args, **target_url.query_args}
        background_tasks.create(build(content, target_url.fragment, combined_dict))
