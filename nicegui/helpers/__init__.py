from .. import core
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


def is_pytest() -> bool:  # DEPRECATED
    """Check if the code is running in pytest.

    .. deprecated::
        Use ``core.is_pytest()`` instead.
    """
    warn_once('helpers.is_pytest() is deprecated, use core.is_pytest() instead')
    return core.is_pytest()


def is_user_simulation() -> bool:  # DEPRECATED
    """Check if the code is running with user simulation.

    .. deprecated::
        Use ``core.is_user_simulation()`` instead.
    """
    warn_once('helpers.is_user_simulation() is deprecated, use core.is_user_simulation() instead')
    return core.is_user_simulation()
