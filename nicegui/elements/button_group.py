from ..element import Element


class ButtonGroup(Element):

    def __init__(self) -> None:
        """Button Group

        This element is based on Quasar's `QBtnGroup <https://quasar.dev/vue-components/button-group>`_ component.
        You must use the same design props on both the parent button group and the children buttons.
        """
        super().__init__(tag='q-btn-group')
