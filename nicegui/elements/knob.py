from ..dependencies import register_component
from ..element import Element
from ..ui import icon

# register_component("knob", __file__, "knob.js")


class Knob(Element):
    def __init__(
        self,
        color: str = "primary",
        center_color: str = "white",
        track_color: str = "secondary",
        size: str = "",
        icon_name: str | None = None,
        icon_color: str = "black",
        icon_size: str = "1rem",
    ):
        """Knob

        This element is based on Quasar's `QKnob <https://quasar.dev/vue-components/knob>`_ component.
        The element is used to take a number input from the user through mouse/touch panning.

        :param color: color name for component, examples: primary, teal-10.
        :param center_color: color name for the center part of the component, examples: primary, teal-10.
        :param track_color: color name for the track of the component, examples: primary, teal-10.
        :param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem.
        :param icon: name for the icon in the center of thecomponent, examples: volume_up, volume_down.
        :param icon_color: color name for the icon in the center of the component, examples: primary, teal-10.
        :param icon_size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem.
        """
        super().__init__("q-knob")

        self._props["color"] = color
        self._props["center-color"] = center_color
        self._props["track-color"] = track_color
        self._props["size"] = size

        if icon_name is not None:
            self._props["show-value"] = True  # FIXME: make it possible to show numerical values, in addition to icons

            with self:
                icon(icon_name)
