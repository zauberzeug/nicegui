import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Config():
    # NOTE: should be in sync with ui.run arguments
    host: str = os.environ.get('HOST', '0.0.0.0')
    port: int = int(os.environ.get('PORT', '8080'))
    title: str = 'NiceGUI'
    reload: bool = True
    favicon: str = 'favicon.ico'
    dark: Optional[bool] = False
    main_page_classes: str = 'q-ma-md column items-start gap-4'
    binding_refresh_interval: float = 0.1
    excludes: List[str] = field(default_factory=list)
