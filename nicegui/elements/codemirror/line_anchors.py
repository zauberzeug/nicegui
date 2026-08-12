from __future__ import annotations

from typing import Any

from typing_extensions import Self

from ...element import Element
from ...events import CodeMirrorAnchorChangeEventArguments, GenericEventArguments, Handler, handle_event


class LineAnchorElement(Element):
    """Mixin tracking CodeMirror line anchors that follow document positions through edits.

    The browser is the source of truth: anchors are remapped by CodeMirror as the document changes
    and the current ``{id: line}`` snapshot is pushed back via the "anchor-positions" event.
    That snapshot is mirrored into the "line-anchors" prop without triggering an update,
    so the prop describes where the anchors actually are rather than where they were declared —
    a re-render then restores the live positions instead of snapping them back.
    Until the browser confirms a deliberate assignment, the prop is sent as-is;
    afterwards it is preserved on unrelated updates.
    """

    def __init__(
        self,
        *,
        line_anchors: dict[str, int] | None = None,
        on_anchor_change: Handler[CodeMirrorAnchorChangeEventArguments] | None = None,
        **kwargs: Any,
    ) -> None:
        # NOTE: validate before super().__init__ registers the element, so a rejected argument
        # does not leave a half-built element behind in the element tree
        _validate(line_anchors or {})
        super().__init__(**kwargs)
        self._anchor_positions: dict[str, int] = {}
        self._anchors_pending = True
        self._anchor_change_handlers: list[Handler[CodeMirrorAnchorChangeEventArguments]] = []
        if line_anchors:
            self._props['line-anchors'] = line_anchors
        self.on('anchor-positions', self._update_anchor_mirror)
        if on_anchor_change is not None:
            self.on_anchor_change(on_anchor_change)

    @property
    def line_anchors(self) -> dict[str, int]:
        """Anchors tracking document positions through edits.

        Assign a ``{id: 1-indexed line}`` dict to declare anchors; reading returns their current positions
        as last reported by the browser, which is the source of truth.
        Maps a caller-chosen ``id`` to its 1-indexed ``line``.
        CodeMirror remaps the underlying position when the document changes,
        so a read briefly lags an assignment until the JS round-trip completes
        and updates asynchronously as later edits remap positions.
        An anchor is dropped only when a deletion spans across its position —
        a full-line delete that starts at the anchor slides it to the following line.

        Lines beyond the end of the document are dropped on the JS side with a warning via NiceGUI's
        logger, just like ``line_tooltips``, so a read never reports a position that was not applied.
        A line below 1 is rejected right away with a ``ValueError``.

        *Added in version 3.16.0*
        """
        return self._anchor_positions

    @line_anchors.setter
    def line_anchors(self, anchors: dict[str, int] | None) -> None:
        anchors = anchors or {}
        _validate(anchors)
        self._anchors_pending = True
        self._props['line-anchors'] = anchors

    def _to_dict(self) -> dict[str, Any]:
        dict_ = super()._to_dict()
        if not self._anchors_pending:
            dict_.setdefault('preserved_props', []).append('line-anchors')
        return dict_

    def on_anchor_change(self, handler: Handler[CodeMirrorAnchorChangeEventArguments]) -> Self:
        """Add a callback to be invoked when tracked anchor positions change.

        *Added in version 3.16.0*
        """
        self._anchor_change_handlers.append(handler)
        return self

    def _update_anchor_mirror(self, e: GenericEventArguments) -> None:
        self._anchor_positions = e.args['anchors']
        self._anchors_pending = False
        # A separate dict keeps a caller mutating the exposed positions from rewriting what we send.
        with self._props.suspend_updates():
            self._props['line-anchors'] = dict(self._anchor_positions)
        for handler in self._anchor_change_handlers:
            # A fresh dict per handler keeps one of them from rewriting the exposed positions or the others' view.
            handle_event(handler, CodeMirrorAnchorChangeEventArguments(
                sender=self, client=self.client, anchors=dict(self._anchor_positions)))


def _validate(anchors: dict[str, int]) -> None:
    for id_, line in anchors.items():
        if line < 1:
            raise ValueError(f'line_anchors: anchor {id_!r} has line {line}, but lines are 1-indexed')
