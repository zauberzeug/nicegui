from typing import Literal, Optional

from ..defaults import DEFAULT_PROPS, resolve_defaults
from ..element import Element
from .mixins.icon_element import IconElement


class Timeline(Element):

    @resolve_defaults
    def __init__(self,
                 *,
                 side: Literal['left', 'right'] = DEFAULT_PROPS['side'] | 'left',
                 layout: Literal['dense', 'comfortable', 'loose'] = DEFAULT_PROPS['layout'] | 'dense',
                 color: Optional[str] = DEFAULT_PROPS['color'] | None,
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
                 body: Optional[str] = DEFAULT_PROPS['body'] | None,
                 *,
                 side: Literal['left', 'right'] = DEFAULT_PROPS['side'] | 'left',
                 heading: bool = DEFAULT_PROPS['heading'] | False,
                 tag: Optional[str] = DEFAULT_PROPS['tag'] | None,
                 icon: Optional[str] = DEFAULT_PROPS['icon'] | None,
                 avatar: Optional[str] = DEFAULT_PROPS['avatar'] | None,
                 title: Optional[str] = DEFAULT_PROPS['title'] | None,
                 subtitle: Optional[str] = DEFAULT_PROPS['subtitle'] | None,
                 color: Optional[str] = DEFAULT_PROPS['color'] | None,
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
