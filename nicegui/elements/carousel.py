from __future__ import annotations

from typing import Any, Callable, Optional, Union, cast

from ..context import context
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Carousel(ValueElement):

    def __init__(self, *,
                 value: Union[str, CarouselSlide, None] = None,
                 on_value_change: Optional[Callable[..., Any]] = None,
                 animated: bool = False,
                 arrows: bool = False,
                 navigation: bool = False,
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
        return value._props['name'] if isinstance(value, CarouselSlide) else value  # pylint: disable=protected-access

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        names = [slide._props['name'] for slide in self]  # pylint: disable=protected-access
        for i, slide in enumerate(self):
            done = i < names.index(value) if value in names else False
            slide.props(f':done={done}')

    def next(self) -> None:
        """Show the next slide."""
        self.run_method('next')

    def previous(self) -> None:
        """Show the previous slide."""
        self.run_method('previous')


class CarouselSlide(DisableableElement):

    def __init__(self, name: Optional[str] = None) -> None:
        """Carousel Slide

        This element represents `Quasar's QCarouselSlide <https://quasar.dev/vue-components/carousel#qcarouselslide-api>`_ component.
        It is a child of a `ui.carousel` element.

        :param name: name of the slide (will be the value of the `ui.carousel` element, auto-generated if `None`)
        """
        super().__init__(tag='q-carousel-slide')
        self.carousel = cast(ValueElement, context.slot.parent)
        name = name or f'slide_{len(self.carousel.default_slot.children)}'
        self._props['name'] = name
        self._classes.append('nicegui-carousel-slide')
        if self.carousel.value is None:
            self.carousel.value = name
