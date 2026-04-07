from typing import Any

from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement
from .step import Step


class Stepper(ValueElement[str | Step | None], default_classes='nicegui-stepper'):

    @resolve_defaults
    def __init__(self, *,
                 value: str | Step | None = DEFAULT_PROPS['model-value'] | None,
                 on_value_change: Handler[ValueChangeEventArguments[str | Step | None]] | None = None,
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
