from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Optional

from ..element import Element

if TYPE_CHECKING:
    from ..single_page_router import SinglePageRouter


class Frame(Element, component='frame.js'):
    """A Frame is a UI slot which contains sub-outlets/views. It provides the container where page content
    is rendered and updated."""

    def __init__(self,
                 router: SinglePageRouter,
                 base_path: str,
                 target_url: Optional[str] = None,
                 included_paths: Optional[list[str]] = None,
                 excluded_paths: Optional[list[str]] = None,
                 use_browser_history: bool = True,
                 on_navigate: Optional[Callable[[str, Optional[bool]], Any]] = None,
                 ):
        """
        :param base_path: The base URL path all relative paths are based on
        :param included_paths: A list of valid path masks which shall be allowed to be opened by the router
        :param excluded_paths: A list of path masks which shall be excluded from the router
        :param use_browser_history: Optional flag to enable or disable the browser history management. Default is True.
        :param target_url: The initial url of the frame
        :param on_navigate: Optional callback which is called when the browser / JavaScript navigates to a new url
        :param user_data: Optional user data which is passed to the builder functions of the frame
        """
        super().__init__()
        self.router = router
        self._props['target_url'] = target_url
        self._props['included_path_masks'] = included_paths if included_paths is not None else []
        self._props['excluded_path_masks'] = excluded_paths if excluded_paths is not None else []
        self._props['base_path'] = base_path
        self._props['browser_history'] = use_browser_history
        self._props['child_frame_paths'] = []
        self.on('open', lambda e: self.handle_navigate(e.args[0], e.args[1]))
        self.on_navigate = on_navigate

    def handle_navigate(self, url: str, history=True):
        """Navigate to a new url

        :param url: The url to navigate to
        :param history: Optional flag to enable or disable the browser history management. Default is True.
        """
        if self.on_navigate is not None:
            self.on_navigate(url, history)

    @property
    def target_url(self) -> str:
        """The current target url of the frame"""
        return self._props['target_url']

    @target_url.setter
    def target_url(self, value: str):
        """Set the target url of the frame"""
        self._props['target_url'] = value

    def clear(self) -> None:
        """Clear the content of the frame and removes all references to sub frames"""
        self._props['child_frame_paths'] = []
        super().clear()

    @property
    def child_frame_paths(self) -> list[str]:
        """The child paths of the frame"""
        return self._props['child_frame_paths']

    @child_frame_paths.setter
    def child_frame_paths(self, paths: list[str]) -> None:
        """Update the child paths of the frame

        :param paths: The list of child paths"""
        self._props['child_frame_paths'] = paths
