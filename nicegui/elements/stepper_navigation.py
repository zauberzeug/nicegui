from ..element import Element


class StepperNavigation(Element):

    def __init__(self, *, wrap: bool = True) -> None:
        """Stepper Navigation

        This element represents `Quasar's QStepperNavigation https://quasar.dev/vue-components/stepper#qsteppernavigation-api>`_ component.

        :param wrap: whether to wrap the content (default: `True`)
        """
        super().__init__('q-stepper-navigation')

        if wrap:
            self._classes.append('wrap')
