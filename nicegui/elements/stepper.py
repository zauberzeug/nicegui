from __future__ import annotations

from typing import Any, cast

from ..context import context
from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..element import Element
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.value_element import ValueElement


class Stepper(ValueElement, default_classes='nicegui-stepper'):

    @resolve_defaults
    def __init__(self, *,
                 value: str | Step | None = DEFAULT_PROPS['model-value'] | None,
                 on_value_change: Handler[ValueChangeEventArguments] | None = None,
                 keep_alive: bool = DEFAULT_PROP | True,
                 ) -> None:
        """Stepper

        This element represents `Quasar's QStepper <https://quasar.dev/vue-components/stepper#qstepper-api>`_ component.
        It contains individual steps.

        To avoid issues with dynamic elements when switching steps,
        this element uses Vue's `keep-alive <https://vuejs.org/guide/built-ins/keep-alive.html>`_ component.
        If client-side performance is an issue, you can disable this feature.

        :param value: `ui.step` or name of the step to be initially selected (default: `None` meaning the first step)
        :param on_value_change: callback to be executed when the selected step changes
        :param keep_alive: whether to use Vue's keep-alive component on the content (default: `True`)
        """
        super().__init__(tag='q-stepper', value=value, on_value_change=on_value_change)
        self._props.set_bool('keep-alive', keep_alive)

    def _value_to_model_value(self, value: Any) -> Any:
        return value.props['name'] if isinstance(value, Step) else value

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        names = [step.props['name'] for step in self]
        for i, step in enumerate(self):
            done = i < names.index(value) if value in names else False
            step.props(f':done={done}')

    def next(self) -> None:
        """Show the next step."""
        self.run_method('next')

    def previous(self) -> None:
        """Show the previous step."""
        self.run_method('previous')


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


class StepperNavigation(Element):

    def __init__(self, *, wrap: bool = True) -> None:
        """Stepper Navigation

        This element represents `Quasar's QStepperNavigation https://quasar.dev/vue-components/stepper#qsteppernavigation-api>`_ component.

        :param wrap: whether to wrap the content (default: `True`)
        """
        super().__init__('q-stepper-navigation')

        if wrap:
            self._classes.append('wrap')
