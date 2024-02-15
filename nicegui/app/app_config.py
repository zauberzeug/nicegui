from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union

from ..dataclasses import KWONLY_SLOTS
from ..language import Language


@dataclass(**KWONLY_SLOTS)
@dataclass
class AppConfig:
    """Represents the configuration for the NiceGUI application.

    The AppConfig class stores various settings and options for the NiceGUI application.
    It provides a convenient way to configure the behavior of the application.

    Attributes:
        endpoint_documentation (Literal['none', 'internal', 'page', 'all']): The level of endpoint documentation to display.
        socket_io_js_query_params (Dict): Additional query parameters to include in the Socket.IO JavaScript connection.
        socket_io_js_extra_headers (Dict): Additional headers to include in the Socket.IO JavaScript connection.
        socket_io_js_transports (List[Literal['websocket', 'polling']]): The preferred transports for the Socket.IO JavaScript connection.
        quasar_config (Dict): Configuration options for the Quasar framework.

        reload (bool): Whether the application should reload on changes.
        title (str): The title of the application.
        viewport (str): The viewport meta tag for the application.
        favicon (Optional[Union[str, Path]]): The path to the favicon file.
        dark (Optional[bool]): Whether to use a dark theme.
        language (Language): The language settings for the application.
        binding_refresh_interval (float): The interval at which to refresh bindings.
        reconnect_timeout (float): The timeout for reconnection attempts.
        tailwind (bool): Whether to use the Tailwind CSS framework.
        prod_js (bool): Whether to use the production JavaScript bundle.
        show_welcome_message (bool): Whether to show a welcome message.

        _has_run_config (bool): Internal flag indicating whether the run config has been added.

    Methods:
        add_run_config: Add the run config to the app config.
        has_run_config: Check if the run config has been added.

    Examples:
        # Create an instance of AppConfig
        config = AppConfig()

        # Add a run config
        config.add_run_config(
            reload=True,
            title="My App",
            viewport="width=device-width, initial-scale=1.0",
            favicon="path/to/favicon.ico",
            dark=True,
            language=Language(),
            binding_refresh_interval=0.5,
            reconnect_timeout=10.0,
            tailwind=True,
            prod_js=False,
            show_welcome_message=True
        )

        # Check if the run config has been added
        has_run_config = config.has_run_config

    """

    endpoint_documentation: Literal['none', 'internal', 'page', 'all'] = 'none'
    socket_io_js_query_params: Dict = field(default_factory=dict)
    socket_io_js_extra_headers: Dict = field(default_factory=dict)
    socket_io_js_transports: List[Literal['websocket', 'polling']] = \
        field(default_factory=lambda: ['websocket', 'polling'])  # NOTE: we favor websocket
    quasar_config: Dict = \
        field(default_factory=lambda: {
            'brand': {
                'primary': '#5898d4',
            },
            'loadingBar': {
                'color': 'primary',
                'skipHijack': False,
            },
        })

    reload: bool = field(init=False)
    title: str = field(init=False)
    viewport: str = field(init=False)
    favicon: Optional[Union[str, Path]] = field(init=False)
    dark: Optional[bool] = field(init=False)
    language: Language = field(init=False)
    binding_refresh_interval: float = field(init=False)
    reconnect_timeout: float = field(init=False)
    tailwind: bool = field(init=False)
    prod_js: bool = field(init=False)
    show_welcome_message: bool = field(init=False)
    _has_run_config: bool = False

    def add_run_config(self,
                       *,
                       reload: bool,
                       title: str,
                       viewport: str,
                       favicon: Optional[Union[str, Path]],
                       dark: Optional[bool],
                       language: Language,
                       binding_refresh_interval: float,
                       reconnect_timeout: float,
                       tailwind: bool,
                       prod_js: bool,
                       show_welcome_message: bool,
                       ) -> None:
        """Add the run config to the app config.

        This method allows you to add a run configuration to the app config.
        The run configuration includes various settings and options that control
        the behavior of the application when it is run.

        Args:
            reload (bool): Whether the application should reload on changes.
            title (str): The title of the application.
            viewport (str): The viewport meta tag for the application.
            favicon (Optional[Union[str, Path]]): The path to the favicon file.
            dark (Optional[bool]): Whether to use a dark theme.
            language (Language): The language settings for the application.
            binding_refresh_interval (float): The interval at which to refresh bindings.
            reconnect_timeout (float): The timeout for reconnection attempts.
            tailwind (bool): Whether to use the Tailwind CSS framework.
            prod_js (bool): Whether to use the production JavaScript bundle.
            show_welcome_message (bool): Whether to show a welcome message.

        Returns:
            None

        """
        self.reload = reload
        self.title = title
        self.viewport = viewport
        self.favicon = favicon
        self.dark = dark
        self.language = language
        self.binding_refresh_interval = binding_refresh_interval
        self.reconnect_timeout = reconnect_timeout
        self.tailwind = tailwind
        self.prod_js = prod_js
        self.show_welcome_message = show_welcome_message
        self._has_run_config = True

    @property
    def has_run_config(self) -> bool:
        """Return whether the run config has been added.

        This property returns a boolean value indicating whether the run config
        has been added to the app config.

        Returns:
            bool: True if the run config has been added, False otherwise.

        """
        return self._has_run_config
