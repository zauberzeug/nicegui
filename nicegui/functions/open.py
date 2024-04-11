from typing import Any, Callable, Union

from ..element import Element
from .navigate import Navigate as navigate


def open(target: Union[Callable[..., Any], str, Element], new_tab: bool = False) -> None:  # pylint: disable=redefined-builtin
    """DEPRECATED: use `ui.navigate.to` instead"""
    navigate.to(target, new_tab)
