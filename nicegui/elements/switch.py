from ..defaults import DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Switch(TextElement, ValueElement, DisableableElement):

    @resolve_defaults
    def __init__(self,
                 text: str = '', *,
                 value: bool | None = DEFAULT_PROPS['model-value'] | False,
                 on_change: Handler[ValueChangeEventArguments] | None = None) -> None:
        """Switch

        This element is based on Quasar's `QToggle <https://quasar.dev/vue-components/toggle>`_ component.

        :param text: the label to display next to the switch
        :param value: whether it should be active initially (default: `False`)
        :param on_change: callback which is invoked when state is changed by the user
        """
        super().__init__(tag='q-toggle', text=text, value=value, on_value_change=on_change)
