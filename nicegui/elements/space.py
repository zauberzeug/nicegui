from ..element import Element


class Space(Element):
    """A space element that fills all available space inside a flexbox container.

    This element is based on Quasar's [QSpace](https://quasar.dev/vue-components/space) component.

    The `Space` element is used to create empty space within a flexbox container. It expands to fill all available space, pushing other elements apart.

    Usage:
        To create a `Space` element, simply instantiate the class:

        ```python
        space = Space()
        ```

    Attributes:
        - `tag` (str): The HTML tag used for the element. Defaults to 'q-space'.

    Note:
        The `Space` element should be used within a flexbox container to achieve the desired effect. It is not intended to be used as a standalone element.

    """

    
    def __init__(self, tag: str = 'q-space') -> None:
        """Space

        Args:
            tag (str, optional): The HTML tag used for the element. Defaults to 'q-space'.

        Returns:
            None

        Raises:
            None

        Notes:
            - The Space element represents a blank space in a graphical user interface.
            - It can be used to create gaps between other elements or to add visual separation.
            - The `tag` parameter allows you to specify the HTML tag used for the element.
                By default, it is set to 'q-space', but you can change it to any valid HTML tag.

        """
        super().__init__('q-space')
