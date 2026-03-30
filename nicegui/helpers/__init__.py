import os

from .elements import require_top_level_layout
from .files import hash_file_path, is_file
from .functions import expects_arguments, is_coroutine_function
from .network import is_port_open, schedule_browser
from .strings import event_type_to_camel_case, kebab_to_camel_case
from .warnings import warn_once

__all__ = [
    'event_type_to_camel_case',
    'expects_arguments',
    'hash_file_path',
    'is_coroutine_function',
    'is_file',
    'is_port_open',
    'is_pytest',
    'is_user_simulation',
    'kebab_to_camel_case',
    'require_top_level_layout',
    'schedule_browser',
    'warn_once',
]


def is_pytest() -> bool:
    """Check if the code is running in pytest."""
    return 'PYTEST_CURRENT_TEST' in os.environ


def is_user_simulation() -> bool:
    """Check if the code is running in with user simulation (see https://nicegui.io/documentation/user)."""
    return 'NICEGUI_USER_SIMULATION' in os.environ
