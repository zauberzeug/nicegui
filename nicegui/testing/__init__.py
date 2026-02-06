try:
    from .screen import Screen, SharedScreen
except ImportError:
    # we simply define Screen as None if selenium is not installed
    # this allows simpler dependency management when only using the "User" fixture
    # (see discussion in #3510)
    Screen = None  # type: ignore
    SharedScreen = None  # type: ignore

from .user import User
from .user_interaction import UserInteraction
from .user_simulation import user_simulation

__all__ = [
    'Screen',
    'SharedScreen',
    'User',
    'UserInteraction',
    'user_simulation',
]
