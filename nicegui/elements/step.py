from typing import cast

from ..context import context
from ..defaults import DEFAULT_PROP, resolve_defaults
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.value_element import ValueElement


class Step(IconElement, DisableableElement, default_classes='nicegui-step'):

    @resolve_defaults
    def __init__(self, name: str, title: str | None = None, icon: str | None = DEFAULT_PROP | None) -> None:
        """Step

        This element represents `Quasar's QStep <https://quasar.dev/vue-components/stepper#qstep-api>`_ component.
        It is a child of a `ui.stepper` element.

        :param name: name of the step (will be the value of the `ui.stepper` element)
        :param title: title of the step (default: `None`, meaning the same as `name`)
        :param icon: icon of the step (default: `None`)
        """
        super().__init__(tag='q-step', icon=icon)
        self._props['name'] = name
        self._props['title'] = title if title is not None else name
        self.stepper = cast(ValueElement, context.slot.parent)
        if self.stepper.value is None:
            self.stepper.value = name
