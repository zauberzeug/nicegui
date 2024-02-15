from typing import Literal, Optional

from nicegui.element import Element


class Timeline(Element):

    def __init__(self,
                 *,
                 side: Literal['left', 'right'] = 'left',
                 layout: Literal['dense', 'comfortable', 'loose'] = 'dense',
                 color: Optional[str] = None,
                 ) -> None:
        """Timeline

        This element represents [Quasar's QTimeline ](https://quasar.dev/vue-components/timeline#qtimeline-api) component.

        - side: Side ("left" or "right"; default: "left").
        - layout: Layout ("dense", "comfortable" or "loose"; default: "dense").
        - color: Color of the icons.
        """
        super().__init__('q-timeline')
        self._props['side'] = side
        self._props['layout'] = layout
        if color is not None:
            self._props['color'] = color


class TimelineEntry(Element):

    def __init__(self,
                 body: Optional[str] = None,
                 *,
                 side: Literal['left', 'right'] = 'left',
                 heading: bool = False,
                 tag: Optional[str] = None,
                 icon: Optional[str] = None,
                 avatar: Optional[str] = None,
                 title: Optional[str] = None,
                 subtitle: Optional[str] = None,
                 color: Optional[str] = None,
                 ) -> None:
        """Timeline Entry

        This element represents [Quasar's QTimelineEntry ](https://quasar.dev/vue-components/timeline#qtimelineentry-api) component.

        - body: Body text.
        - side: Side ("left" or "right"; default: "left").
        - heading: Whether the timeline entry is a heading.
        - tag: HTML tag name to be used if it is a heading.
        - icon: Icon name.
        - avatar: Avatar URL.
        - title: Title text.
        - subtitle: Subtitle text.
        - color: Color or the timeline.
        """
        super().__init__('q-timeline-entry')
        if body is not None:
            self._props['body'] = body
        self._props['side'] = side
        self._props['heading'] = heading
        if tag is not None:
            self._props['tag'] = tag
        if color is not None:
            self._props['color'] = color
        if icon is not None:
            self._props['icon'] = icon
        if avatar is not None:
            self._props['avatar'] = avatar
        if title is not None:
            self._props['title'] = title
        if subtitle is not None:
            self._props['subtitle'] = subtitle
        self._classes.append('nicegui-timeline-entry')
