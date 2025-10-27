from ..element import Element


class AspectRatio(Element):

    def __init__(self, *, ratio: float) -> None:
        """Aspect Ratio

        This element is based on Quasar's `QResponsive <https://quasar.dev/vue-components/responsive>`_ component.
        It helps to preserve a target aspect ratio for the content it wraps.

        The underlying Quasar component requires exactly one direct child.
        When adding multiple NiceGUI elements, wrap them in an additional container
        such as ``ui.row`` or ``ui.column`` to satisfy this constraint.
        Avoid wrapping Quasar components that already provide a ``ratio`` prop
        such as ``ui.image`` or ``ui.video``, as well as components that impose a fixed height.

        *Added in version 3.2.0*

        :param ratio: ratio of width to height which should be preserved
        """
        super().__init__('q-responsive')

        self._props['ratio'] = ratio
