from __future__ import annotations

from typing import Any

from typing_extensions import Self

from ...element import Element
from ...events import (
    CodeMirrorFocusChangeEventArguments,
    CodeMirrorGeometryChangeEventArguments,
    CodeMirrorSelectionChangeEventArguments,
    CodeMirrorViewportChangeEventArguments,
    Handler,
    handle_event,
)


class SignalElement(Element):
    """Mixin reporting CodeMirror editor state (selection, focus, visible lines, geometry) to Python.

    The frontend emits a signal only while a listener for its event is registered
    and only when its payload differs from the last one sent.
    Rate limiting is left to the ``throttle`` of the event listener.
    """

    def __init__(
        self,
        *,
        on_selection_change: Handler[CodeMirrorSelectionChangeEventArguments] | None = None,
        on_focus_change: Handler[CodeMirrorFocusChangeEventArguments] | None = None,
        on_viewport_change: Handler[CodeMirrorViewportChangeEventArguments] | None = None,
        on_geometry_change: Handler[CodeMirrorGeometryChangeEventArguments] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        if on_selection_change is not None:
            self.on_selection_change(on_selection_change)
        if on_focus_change is not None:
            self.on_focus_change(on_focus_change)
        if on_viewport_change is not None:
            self.on_viewport_change(on_viewport_change)
        if on_geometry_change is not None:
            self.on_geometry_change(on_geometry_change)

    def on_selection_change(self, handler: Handler[CodeMirrorSelectionChangeEventArguments]) -> Self:
        """Add a callback for cursor selection changes (line + column).

        Fires on selection moves and on document edits that shift the cursor line or column.
        ``from_line``/``to_line`` span the main selection (equal and ``empty`` is ``True`` for a bare cursor).
        ``column`` counts Unicode code points, so it indexes ``value`` the same way Python does.

        *Added in version 3.18.0*
        """
        self.on('selection-change', lambda e: handle_event(handler, CodeMirrorSelectionChangeEventArguments(
            sender=self,
            client=self.client,
            line=e.args['line'],
            column=e.args['column'],
            from_line=e.args['from_line'],
            to_line=e.args['to_line'],
            empty=e.args['empty'],
        )), throttle=0.03)
        return self

    def on_focus_change(self, handler: Handler[CodeMirrorFocusChangeEventArguments]) -> Self:
        """Add a callback for editor focus changes.

        *Added in version 3.18.0*
        """
        self.on('focus-change', lambda e: handle_event(handler, CodeMirrorFocusChangeEventArguments(
            sender=self,
            client=self.client,
            focused=e.args['focused'],
        )))
        return self

    def on_viewport_change(self, handler: Handler[CodeMirrorViewportChangeEventArguments]) -> Self:
        """Add a callback for changes of the visible line range.

        ``from_line``/``to_line`` are the first and last line shown in the editor's scroll area,
        including lines that are only partly visible.
        Whether the surrounding page clips the editor itself is not taken into account.

        *Added in version 3.18.0*
        """
        self.on('viewport-change', lambda e: handle_event(handler, CodeMirrorViewportChangeEventArguments(
            sender=self,
            client=self.client,
            from_line=e.args['from_line'],
            to_line=e.args['to_line'],
        )), throttle=0.1)
        return self

    def on_geometry_change(self, handler: Handler[CodeMirrorGeometryChangeEventArguments]) -> Self:
        """Add a callback for editor geometry changes (width, height, content height).

        *Added in version 3.18.0*
        """
        self.on('geometry-change', lambda e: handle_event(handler, CodeMirrorGeometryChangeEventArguments(
            sender=self,
            client=self.client,
            width=e.args['width'],
            height=e.args['height'],
            content_height=e.args['content_height'],
        )), throttle=0.1)
        return self
