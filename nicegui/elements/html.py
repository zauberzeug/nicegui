from .mixins.content_element import ContentElement


class Html(ContentElement):
    """Represents an HTML element that renders arbitrary HTML onto the page.

    This class is a subclass of `ContentElement` and can be used to display custom HTML code on the page.
    It provides methods to add HTML code into the head or body of the document.

    Attributes:
        tag (str): The HTML tag to be used for rendering the element. By default, it is set to 'div'.
        content (str): The HTML code to be displayed.

    Example:
        html_element = Html('<h1>Hello, World!</h1>')
    """

    def __init__(self, content: str = '') -> None:
        """Initializes a new instance of the Html class.

        Args:
            content (str, optional): The HTML code to be displayed. Defaults to an empty string.
        """
        super().__init__(tag='div', content=content)
        