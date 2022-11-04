import justpy as jp

from .element import Element
from ..binding import BindableProperty, BindTextMixin


class _QBadge(jp.QBadge):
    """QBadge
    Need to override QBadge in order to provide an additional property 'text'.
    setattr() approach won't work due to QDiv.__setattr__ :-(
    """

    @property
    def text(self) -> str:
        return self.label

    @text.setter
    def text(self, value: str):
        self.label = value


class Badge(Element, BindTextMixin):
    text = BindableProperty()

    def __init__(self, text: str = '', *,
                 color: str = 'blue', text_color: str = 'white', outline: bool = False) -> None:
        """Badge

        A badge element wrapping Quasar's
        `QBadge <https://v1.quasar.dev/vue-components/badge>`_ component.

        :param text: the initial value of the text field
        :param color: the color name for component from the Quasar Color Palette (default: "blue")
        :param text_color: overrides text color (if needed); color name from the Quasar Color Palette (default: "white")
        :param outline: use 'outline' design (colored text and borders only) (default: False)
        """
        view = _QBadge(color=color, text_color=text_color, delete_flag=False, temp=True, align='middle',
                       outline=outline, text=text)
        super().__init__(view)

        self.text = text
        self.bind_text_to(self.view, 'text')

    def set_text(self, text: str):
        self.text = text
