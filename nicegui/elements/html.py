from .mixins.content_element import ContentElement


class Html(ContentElement):

    def __init__(self, content: str = '', *, tag: str = 'div') -> None:
        """HTML Element

        Renders arbitrary HTML onto the page, wrapped in the specified tag.
        `Tailwind <https://tailwindcss.com/>`_ can be used for styling.
        You can also use `ui.add_head_html` to add html code into the head of the document and `ui.add_body_html`
        to add it into the body.

        :param content: the HTML code to be displayed
        :param tag: the HTML tag to wrap the content in (default: "div")
        """
        super().__init__(tag=tag, content=content)
