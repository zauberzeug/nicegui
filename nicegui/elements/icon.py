from ..defaults import DEFAULT_PROP, resolve_defaults
from .mixins.color_elements import TextColorElement
from .mixins.name_element import NameElement


class Icon(NameElement, TextColorElement):

    @resolve_defaults
    def __init__(self,
                 name: str,
                 *,
                 size: str | None = DEFAULT_PROP | None,
                 color: str | None = DEFAULT_PROP | None,
                 ) -> None:
        """Icon

        This element is based on Quasar's `QIcon <https://quasar.dev/vue-components/icon>`_ component.

        `Here <https://fonts.google.com/icons?icon.set=Material+Icons>`_ is a reference of possible names.

        :param name: name of the icon (snake case, e.g. `add_circle`)
        :param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem
        :param color: icon color (either a Quasar, Tailwind, or CSS color or `None`, default: `None`)
        """
        super().__init__(tag='q-icon', name=name, text_color=color)

        self._props.set_optional('size', size)
