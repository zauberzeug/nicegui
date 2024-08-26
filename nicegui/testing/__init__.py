try:
    from .screen import Screen
except ImportError as e:
    # we simply define Screen as None if selenium is not installed
    # this allows simpler dependency management when only using the "User" fixture
    class Screen:  # type: ignore
        error = e

        def __init__(self, *args, **kwargs):
            raise RuntimeError('Screen is not available') from self.error

        def __getattr__(self, name):
            raise RuntimeError('Screen is not available') from self.error

from .user import User
from .user_interaction import UserInteraction

__all__ = [
    'Screen',
    'User',
    'UserInteraction',
]
