from typing import Any

from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .carousel_slide import CarouselSlide
from .mixins.value_element import ValueElement


class Carousel(ValueElement[str | CarouselSlide | None]):

    @resolve_defaults
    def __init__(self, *,
                 value: str | CarouselSlide | None = DEFAULT_PROPS['model-value'] | None,
                 on_value_change: Handler[ValueChangeEventArguments[str | CarouselSlide | None]] | None = None,
                 animated: bool = DEFAULT_PROP | False,
                 arrows: bool = DEFAULT_PROP | False,
                 navigation: bool = DEFAULT_PROP | False,
                 ) -> None:
        """Carousel

        This element represents `Quasar's QCarousel <https://quasar.dev/vue-components/carousel#qcarousel-api>`_ component.
        It contains individual carousel slides.

        :param value: `ui.carousel_slide` or name of the slide to be initially selected (default: `None` meaning the first slide)
        :param on_value_change: callback to be executed when the selected slide changes
        :param animated: whether to animate slide transitions (default: `False`)
        :param arrows: whether to show arrows for manual slide navigation (default: `False`)
        :param navigation: whether to show navigation dots for manual slide navigation (default: `False`)
        """
        super().__init__(tag='q-carousel', value=value, on_value_change=on_value_change)
        self._props['animated'] = animated
        self._props['arrows'] = arrows
        self._props['navigation'] = navigation

    def _value_to_model_value(self, value: Any) -> Any:
        return value.props['name'] if isinstance(value, CarouselSlide) else value

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        names = [slide.props['name'] for slide in self.default_slot]
        for i, slide in enumerate(self):
            done = i < names.index(value) if value in names else False
            slide.props(f':done={done}')

    def next(self) -> None:
        """Show the next slide."""
        self.run_method('next')

    def previous(self) -> None:
        """Show the previous slide."""
        self.run_method('previous')
