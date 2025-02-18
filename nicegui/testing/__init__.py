try:
    from .screen import Screen
except ImportError:
    # we simply define Screen as None if selenium is not installed
    # this allows simpler dependency management when only using the "User" fixture
    # (see discussion in #3510)
    Screen = None  # type: ignore

from .user import User
from .user_interaction import UserInteraction

__all__ = [
    'Screen',
    'User',
    'UserInteraction',
]
