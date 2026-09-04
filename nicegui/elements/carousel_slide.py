from typing import cast

from ..context import context
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class CarouselSlide(DisableableElement, default_classes='nicegui-carousel-slide'):

    def __init__(self, name: str | None = None) -> None:
        """Carousel Slide

        This element represents `Quasar's QCarouselSlide <https://quasar.dev/vue-components/carousel#qcarouselslide-api>`_ component.
        It is a child of a `ui.carousel` element.

        :param name: name of the slide (will be the value of the `ui.carousel` element, auto-generated if `None`)
        """
        super().__init__(tag='q-carousel-slide')
        self.carousel = cast(ValueElement, context.slot.parent)
        name = name or f'slide_{len(self.carousel.default_slot.children)}'
        self._props['name'] = name
        if self.carousel.value is None:
            self.carousel.value = name
