from __future__ import annotations

from typing import Any, Callable, Optional, Union, cast

from .. import context
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Carousel(ValueElement):
    """A carousel element that represents a collection of carousel slides.

    This element represents [Quasar's QCarousel ](https://quasar.dev/vue-components/carousel#qcarousel-api) component.
    It contains individual carousel slides.

    Args:
    
        - value (Union[str, CarouselSlide, None], optional): The initial selected slide. It can be the name of the slide or a `CarouselSlide` instance. Defaults to `None`.
        - on_value_change (Optional[Callable[..., Any]], optional): A callback function to be executed when the selected slide changes. Defaults to `None`.
        - animated (bool, optional): Whether to animate slide transitions. Defaults to `False`.
        - arrows (bool, optional): Whether to show arrows for manual slide navigation. Defaults to `False`.
        - navigation (bool, optional): Whether to show navigation dots for manual slide navigation. Defaults to `False`.

    Attributes:
    
        - tag (str): The HTML tag for the carousel element.
        - _props (Dict[str, Any]): The dictionary of properties for the carousel element.

    Methods:
    
        - _value_to_model_value(value: Any) -> Any: Converts the value to the model value.
        - _handle_value_change(value: Any) -> None: Handles the value change event.
        - next() -> None: Shows the next slide.
        - previous() -> None: Shows the previous slide.
    """

    def __init__(self, *,
                 value: Union[str, CarouselSlide, None] = None,
                 on_value_change: Optional[Callable[..., Any]] = None,
                 animated: bool = False,
                 arrows: bool = False,
                 navigation: bool = False,
                 ) -> None:
        """Carousel

        This element represents [Quasar's QCarousel] (https://quasar.dev/vue-components/carousel#qcarousel-api) component.
        It contains individual carousel slides.

        Args:
        
            - value (Union[str, CarouselSlide, None], optional): The initial selected slide. It can be the name of the slide or a `CarouselSlide` instance. Defaults to `None`.
            - on_value_change (Optional[Callable[..., Any]], optional): A callback function to be executed when the selected slide changes. Defaults to `None`.
            - animated (bool, optional): Whether to animate slide transitions. Defaults to `False`.
            - arrows (bool, optional): Whether to show arrows for manual slide navigation. Defaults to `False`.
            - navigation (bool, optional): Whether to show navigation dots for manual slide navigation. Defaults to `False`.
        """
        super().__init__(tag='q-carousel', value=value, on_value_change=on_value_change)
        self._props['animated'] = animated
        self._props['arrows'] = arrows
        self._props['navigation'] = navigation

    def _value_to_model_value(self, value: Any) -> Any:
        """Convert the value to the model value.

        Args:
        
            - value (Any): The value to be converted.

        Returns:
            - Any: The converted model value.
        """
        return value._props['name'] if isinstance(value, CarouselSlide) else value  # pylint: disable=protected-access

    def _handle_value_change(self, value: Any) -> None:
        """Handle the value change event.

        Args:
        
            - value (Any): The new value.
        """
        super()._handle_value_change(value)
        names = [slide._props['name'] for slide in self]  # pylint: disable=protected-access
        for i, slide in enumerate(self):
            done = i < names.index(value) if value in names else False
            slide.props(f':done={done}')

    def next(self) -> None:
            """Show the next slide.

            This method is used to display the next slide in the carousel.
            It internally calls the 'next' method of the carousel to update the display.

            Returns:
                None

            Example:
                carousel = Carousel()
                carousel.next()
            """
            self.run_method('next')

    def previous(self) -> None:
        """Show the previous slide.

        This method is used to display the previous slide in the carousel.
        It internally calls the 'previous' method to perform the necessary actions.

        Usage:
            To show the previous slide, simply call this method on the Carousel object.

        Example:
            carousel = Carousel()
            carousel.previous()

        Note:
            This method assumes that the carousel has at least two slides. If the carousel
            has only one slide, calling this method will have no effect.

        Returns:
            None
        """
        self.run_method('previous')
        

class CarouselSlide(DisableableElement):
    """Represents a slide in a carousel.

    This class represents a slide in a carousel component. It is a child element of a `ui.carousel` element.

    Attributes:
        name (str): The name of the slide. If not provided, it will be auto-generated based on the number of slides in the carousel.
    """

    def __init__(self, name: Optional[str] = None) -> None:
        """Carousel Slide

        This element represents [Quasar's QCarouselSlide ](https://quasar.dev/vue-components/carousel#qcarouselslide-api) component.
        It is a child of a `ui.carousel` element.
                
        Args:
            name (str, optional): The name of the slide. Defaults to None.

        Notes:
            - The `name` parameter will be used as the value of the `ui.carousel` element.
            - If `name` is not provided, it will be auto-generated based on the number of slides in the carousel.
        """
        super().__init__(tag='q-carousel-slide')
        self.carousel = cast(ValueElement, context.get_slot().parent)
        name = name or f'slide_{len(self.carousel.default_slot.children)}'
        self._props['name'] = name
        self._classes.append('nicegui-carousel-slide')
        if self.carousel.value is None:
            self.carousel.value = name
