import warnings
from functools import wraps

warnings.simplefilter('always', DeprecationWarning)


def deprecated(func: type, old_name: str, new_name: str, issue: int) -> type:
    @wraps(func)
    def wrapped(*args, **kwargs):
        url = f'https://github.com/zauberzeug/nicegui/issues/{issue}'
        warnings.warn(DeprecationWarning(f'{old_name} is deprecated, use {new_name} instead ({url})'))
        return func(*args, **kwargs)
    return wrapped
