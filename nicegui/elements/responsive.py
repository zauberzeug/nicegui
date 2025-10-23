from typing import Optional

from ..element import Element


class Responsive(Element):

    def __init__(
        self,
        *,
        ratio: Optional[float] = None,
    ) -> None:
        """Responsive

        This element is based on Quasar's `QResponsive <https://quasar.dev/vue-components/responsive>`_ component.
        It helps to preserve a target aspect ratio for the content it wraps.

        The underlying Quasar component requires exactly one direct child. When adding multiple
        NiceGUI elements, wrap them in an additional container such as :func:`ui.column` or
        :func:`ui.row` to satisfy this constraint. Avoid wrapping Quasar components that already
        provide a ``ratio`` prop such as :func:`ui.image` or :func:`ui.video`, as well as
        components that impose a fixed height.

        :param ratio: ratio of width to height which should be preserved (e.g. ``16/9``).
            When providing the ratio as a string, specify the decimal value directly instead
            of a computed expression (e.g. use ``"1.7777"`` instead of ``"16/9"``).
        """
        super().__init__('q-responsive')

        if ratio is not None:
            self._props['ratio'] = ratio
