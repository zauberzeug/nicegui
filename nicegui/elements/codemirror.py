from nicegui.element import Element


class CodeMirror(Element, component='codemirror.js'):

    def __init__(self) -> None:
        """CodeMirror

        CodeMirror is a versatile text editor implemented in JavaScript for the browser.
        """
        super().__init__()
