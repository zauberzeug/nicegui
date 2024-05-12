import inspect
from typing import Optional, Any, Callable

from nicegui import ui, background_tasks


class RouterFrame(ui.element, component='router_frame.js'):
    """The RouterFrame is a special element which is used by the SinglePageRouter to exchange the content of
    the current page with the content of the new page. It serves as container and overrides the browser's history
    management to prevent the browser from reloading the whole page."""

    def __init__(self,
                 base_path: str,
                 target_url: Optional[str] = None,
                 included_paths: Optional[list[str]] = None,
                 excluded_paths: Optional[list[str]] = None,
                 use_browser_history: bool = True,
                 on_navigate: Optional[Callable[[str, Optional[bool]], Any]] = None,
                 user_data: Optional[dict] = None
                 ):
        """
        :param base_path: The base URL path all relative paths are based on
        :param included_paths: A list of valid path masks which shall be allowed to be opened by the router
        :param excluded_paths: A list of path masks which shall be excluded from the router
        :param use_browser_history: Optional flag to enable or disable the browser history management. Default is True.
        :param target_url: The initial url of the router frame
        :param on_navigate: Optional callback which is called when the browser / JavaScript navigates to a new url
        :param user_data: Optional user data which is passed to the builder functions of the router frame
        """
        super().__init__()
        included_masks = []
        excluded_masks = []
        if included_paths is not None:
            for path in included_paths:
                cleaned = path.rstrip('/')
                included_masks.append(cleaned)
                included_masks.append(cleaned + '/*')
        if excluded_paths is not None:
            for path in excluded_paths:
                cleaned = path.rstrip('/')
                excluded_masks.append(cleaned)
                excluded_masks.append(cleaned + '/*')
        self._props['target_url'] = target_url
        self._props['included_path_masks'] = included_masks
        self._props['excluded_path_masks'] = excluded_masks
        self._props['base_path'] = base_path
        self._props['browser_history'] = use_browser_history
        self._props['child_frames'] = []
        self.on('open', lambda e: self.handle_navigate(e.args[0], e.args[1]))
        self.on_navigate = on_navigate
        self.user_data = user_data if user_data is not None else {}

    def handle_navigate(self, url: str, history=True):
        """Navigate to a new url

        :param url: The url to navigate to
        :param history: Optional flag to enable or disable the browser history management. Default is True.
        """
        if self.on_navigate is not None:
            self.on_navigate(url, history)

    @property
    def target_url(self) -> str:
        """The current target url of the router frame"""
        return self._props['target_url']

    @target_url.setter
    def target_url(self, value: str):
        """Set the target url of the router frame"""
        self._props['target_url'] = value

    def update_content(self, builder, builder_kwargs, title, target_fragment,
                       sync=False):
        """Update the content of the router frame

        :param builder: The builder function which builds the content of the page
        :param builder_kwargs: The keyword arguments to pass to the builder function
        :param title: The title of the page
        :param target_fragment: The fragment to navigate to after the content has been loaded
        :param sync: Optional flag to define if the content should be updated synchronously. Default is False."""

        def exec_builder():
            """Execute the builder function with the given keyword arguments"""
            self.run_safe(builder, **builder_kwargs)

        async def build() -> None:
            with self:
                exec_builder()
                if target_fragment is not None:
                    await ui.run_javascript(f'window.location.href = "#{target_fragment}";')

        if sync:
            with self:
                exec_builder()
                if target_fragment is not None:
                    ui.run_javascript(f'window.location.href = "#{target_fragment}";')
        else:
            background_tasks.create(build())

    def clear(self) -> None:
        """Clear the content of the router frame and removes all references to sub frames"""
        self._props['child_frame_paths'] = []
        super().clear()

    @property
    def child_frame_paths(self) -> list[str]:
        """The child paths of the router frame"""
        return self._props['child_frame_paths']

    @child_frame_paths.setter
    def child_frame_paths(self, paths: list[str]) -> None:
        """Update the child paths of the router frame

        :param paths: The list of child paths"""
        self._props['child_frame_paths'] = paths

    @staticmethod
    def run_safe(builder, type_check: bool = True, **kwargs) -> Any:
        """Run a builder function but only pass the keyword arguments which are expected by the builder function

        :param builder: The builder function
        :param type_check: Optional flag to enable or disable the type checking of the keyword arguments.
            Default is True.
        :param kwargs: The keyword arguments to pass to the builder function
        """
        sig = inspect.signature(builder)
        args = sig.parameters.keys()
        has_kwargs = any([param.kind == inspect.Parameter.VAR_KEYWORD for param in
                          inspect.signature(builder).parameters.values()])
        if type_check:
            for func_param_name, func_param_info in sig.parameters.items():
                if func_param_name not in kwargs:
                    continue
                if func_param_info.annotation is inspect.Parameter.empty:
                    continue
                # ensure type is correct
                if not isinstance(kwargs[func_param_name], func_param_info.annotation):
                    raise ValueError(f'Invalid type for parameter {func_param_name}, '
                                     f'expected {func_param_info.annotation}')

        filtered = {k: v for k, v in kwargs.items() if k in args} if not has_kwargs else kwargs
        return builder(**filtered)
