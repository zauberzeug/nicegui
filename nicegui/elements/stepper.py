from __future__ import annotations

from typing import Any, Callable, Optional, Union, cast

from ..context import context
from ..element import Element
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Stepper(ValueElement):

    def __init__(self, *,
                 value: Union[str, Step, None] = None,
                 on_value_change: Optional[Callable[..., Any]] = None,
                 keep_alive: bool = True,
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
        self._props['keep-alive'] = keep_alive
        self._classes.append('nicegui-stepper')

    def _value_to_model_value(self, value: Any) -> Any:
        return value._props['name'] if isinstance(value, Step) else value  # pylint: disable=protected-access

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        names = [step._props['name'] for step in self]  # pylint: disable=protected-access
        for i, step in enumerate(self):
            done = i < names.index(value) if value in names else False
            step.props(f':done={done}')

    def next(self) -> None:
        """Show the next step."""
        self.run_method('next')

    def previous(self) -> None:
        """Show the previous step."""
        self.run_method('previous')


class Step(DisableableElement):

    def __init__(self, name: str, title: Optional[str] = None, icon: Optional[str] = None) -> None:
        """Step

        This element represents `Quasar's QStep <https://quasar.dev/vue-components/stepper#qstep-api>`_ component.
        It is a child of a `ui.stepper` element.

        :param name: name of the step (will be the value of the `ui.stepper` element)
        :param title: title of the step (default: `None`, meaning the same as `name`)
        :param icon: icon of the step (default: `None`)
        """
        super().__init__(tag='q-step')
        self._props['name'] = name
        self._props['title'] = title if title is not None else name
        self._classes.append('nicegui-step')
        if icon:
            self._props['icon'] = icon
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
