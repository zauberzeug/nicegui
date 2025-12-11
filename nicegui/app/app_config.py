from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional, Union

from ..dataclasses import KWONLY_SLOTS
from ..language import Language


@dataclass(**KWONLY_SLOTS)
class AppConfig:
    endpoint_documentation: Literal['none', 'internal', 'page', 'all'] = 'none'
    socket_io_js_query_params: dict = field(default_factory=dict)
    socket_io_js_extra_headers: dict = field(default_factory=dict)
    socket_io_js_transports: list[Literal['websocket', 'polling']] = \
        field(default_factory=lambda: ['websocket', 'polling'])  # NOTE: we favor websocket
    quasar_config: dict = \
        field(default_factory=lambda: {
            'brand': {
                'primary': '#5898d4',
            },
            'loadingBar': {
                'color': 'primary',
                'skipHijack': False,
            },
        })
    vue_config_script: str = r'''
        app.use(Quasar, {config: vue_config});
        Quasar.lang.set(Quasar.lang[language.replace('-', '')]);
        Quasar.Dark.set(dark === None ? "auto" : dark);
    '''

    reload: bool = field(init=False)
    title: str = field(init=False)
    viewport: str = field(init=False)
    favicon: Optional[Union[str, Path]] = field(init=False)
    dark: Optional[bool] = field(init=False)
    language: Language = field(init=False)
    binding_refresh_interval: Optional[float] = field(init=False)
    reconnect_timeout: float = field(init=False)
    message_history_length: int = field(init=False)
    cache_control_directives: str = field(init=False)
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
                       binding_refresh_interval: Optional[float],
                       reconnect_timeout: float,
                       message_history_length: int,
                       cache_control_directives: str = 'public, max-age=31536000, immutable, stale-while-revalidate=31536000',
                       tailwind: bool,
                       prod_js: bool,
                       show_welcome_message: bool,
                       ) -> None:
        """Add the run config to the app config."""
        self.reload = reload
        self.title = title
        self.viewport = viewport
        self.favicon = favicon
        self.dark = dark
        self.language = language
        self.binding_refresh_interval = binding_refresh_interval
        self.reconnect_timeout = reconnect_timeout
        self.message_history_length = message_history_length
        self.cache_control_directives = cache_control_directives
        self.tailwind = tailwind
        self.prod_js = prod_js
        self.show_welcome_message = show_welcome_message
        self._has_run_config = True

    @property
    def has_run_config(self) -> bool:
        """Return whether the run config has been added."""
        return self._has_run_config
