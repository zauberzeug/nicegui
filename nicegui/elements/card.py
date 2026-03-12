from typing import Literal

from typing_extensions import Self

from ..element import Element


class Card(Element, default_classes='nicegui-card'):

    def __init__(self, *,
                 align_items: Literal['start', 'end', 'center', 'baseline', 'stretch'] | None = None,
                 ) -> None:
        """Card

        This element is based on Quasar's `QCard <https://quasar.dev/vue-components/card>`_ component.
        It provides a container with a dropped shadow.

        Note:
        In contrast to this element,
        the original QCard has no padding by default and hides outer borders and shadows of nested elements.
        If you want the original behavior, use the `tight` method.

        *Updated in version 2.0.0: Don't hide outer borders and shadows of nested elements anymore.*

        :param align_items: alignment of the items in the card ("start", "end", "center", "baseline", or "stretch"; default: `None`)
        """
        super().__init__('q-card')
        if align_items:
            self._classes.append(f'items-{align_items}')

    def tight(self) -> Self:
        """Remove padding and gaps between nested elements."""
        return self.classes('nicegui-card-tight')


class CardSection(Element):

    def __init__(self) -> None:
        """Card Section

        This element is based on Quasar's `QCardSection <https://quasar.dev/vue-components/card#qcardsection-api>`_ component.
        """
        super().__init__('q-card-section')


class CardActions(Element):

    def __init__(self) -> None:
        """Card Actions

        This element is based on Quasar's `QCardActions <https://quasar.dev/vue-components/card#qcardactions-api>`_ component.
        """
        super().__init__('q-card-actions')
