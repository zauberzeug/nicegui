from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union

from .dataclasses import KWONLY_SLOTS
from .language import Language


@dataclass(**KWONLY_SLOTS)
class AppConfig:
    reload: bool
    title: str
    viewport: str
    favicon: Optional[Union[str, Path]]
    dark: Optional[bool]
    language: Language
    binding_refresh_interval: float
    reconnect_timeout: float
    tailwind: bool
    prod_js: bool


@dataclass(**KWONLY_SLOTS)
class ExtraConfig:
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
