from ..element import Element


class Column(Element):
    """A container element that arranges its child elements in a column.

    The `Column` class provides a container element that arranges its child elements in a column layout.
    It inherits from the `Element` class.

    Attributes:
        _classes (List[str]): A list of CSS classes applied to the column element.

    Args:
        wrap (bool, optional): Whether to wrap the content within the column. Defaults to False.

    Example:
        column = Column(wrap=True)
        column.add_child(child_element)
    """

    def __init__(self, *, wrap: bool = False) -> None:
        """Initialize the Column element.

        Args:
            wrap (bool, optional): Whether to wrap the content within the column. Defaults to False.
        """
        super().__init__('div')
        self._classes.append('nicegui-column')

        if wrap:
            self._classes.append('wrap')
