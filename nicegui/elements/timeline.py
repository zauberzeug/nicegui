from typing import Literal

from ..defaults import DEFAULT_PROP, resolve_defaults
from ..element import Element
from .mixins.icon_element import IconElement


class Timeline(Element):

    @resolve_defaults
    def __init__(self,
                 *,
                 side: Literal['left', 'right'] = DEFAULT_PROP | 'left',
                 layout: Literal['dense', 'comfortable', 'loose'] = DEFAULT_PROP | 'dense',
                 color: str | None = DEFAULT_PROP | None,
                 ) -> None:
        """Timeline

        This element represents `Quasar's QTimeline <https://quasar.dev/vue-components/timeline#qtimeline-api>`_ component.

        :param side: Side ("left" or "right"; default: "left").
        :param layout: Layout ("dense", "comfortable" or "loose"; default: "dense").
        :param color: Color of the icons.
        """
        super().__init__('q-timeline')
        self._props['side'] = side
        self._props['layout'] = layout
        self._props.set_optional('color', color)


class TimelineEntry(IconElement, default_classes='nicegui-timeline-entry'):

    @resolve_defaults
    def __init__(self,
                 body: str | None = DEFAULT_PROP | None,
                 *,
                 side: Literal['left', 'right'] = DEFAULT_PROP | 'left',
                 heading: bool = DEFAULT_PROP | False,
                 tag: str | None = DEFAULT_PROP | None,
                 icon: str | None = DEFAULT_PROP | None,
                 avatar: str | None = DEFAULT_PROP | None,
                 title: str | None = DEFAULT_PROP | None,
                 subtitle: str | None = DEFAULT_PROP | None,
                 color: str | None = DEFAULT_PROP | None,
                 ) -> None:
        """Timeline Entry

        This element represents `Quasar's QTimelineEntry <https://quasar.dev/vue-components/timeline#qtimelineentry-api>`_ component.

        :param body: Body text.
        :param side: Side ("left" or "right"; default: "left").
        :param heading: Whether the timeline entry is a heading.
        :param tag: HTML tag name to be used if it is a heading.
        :param icon: Icon name.
        :param avatar: Avatar URL.
        :param title: Title text.
        :param subtitle: Subtitle text.
        :param color: Color or the timeline.
        """
        super().__init__(tag='q-timeline-entry', icon=icon)
        self._props.set_optional('body', body)
        self._props['side'] = side
        self._props['heading'] = heading
        self._props.set_optional('tag', tag)
        self._props.set_optional('color', color)
        self._props.set_optional('avatar', avatar)
        self._props.set_optional('title', title)
        self._props.set_optional('subtitle', subtitle)
