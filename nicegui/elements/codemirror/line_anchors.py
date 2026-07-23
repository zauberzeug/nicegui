from __future__ import annotations

from typing import Any

from typing_extensions import Self

from ...element import Element
from ...events import CodeMirrorAnchorChangeEventArguments, GenericEventArguments, Handler, handle_event


class LineAnchorElement(Element):
    """Mixin tracking CodeMirror line anchors that follow document positions through edits.

    The browser is the source of truth: anchors are remapped by CodeMirror as the document changes and
    the current ``{id: line}`` snapshot is pushed back via the "anchor-positions" event. The declared
    positions are mirrored into the "line-anchors" prop, while ``_anchor_positions`` mirrors the live
    positions on the server. The ``line-anchors`` prop is preserved on unrelated updates so a re-broadcast
    does not snap remapped anchors back to their declared lines.
    """

    def __init__(
        self,
        *,
        line_anchors: dict[str, int] | None = None,
        on_anchor_change: Handler[CodeMirrorAnchorChangeEventArguments] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._anchor_positions: dict[str, int] = {}
        self._apply_anchors = True
        self._props['line-anchors'] = line_anchors or {}
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

        Lines exceeding the current document length are clamped to the last line on the JS side
        (a warning is emitted via NiceGUI's logger).

        *Added in version 3.14.0*
        """
        return dict(self._anchor_positions)

    @line_anchors.setter
    def line_anchors(self, anchors: dict[str, int] | None) -> None:
        self._props['line-anchors'] = anchors or {}
        self._apply_anchors = True

    def _to_dict(self) -> dict[str, Any]:
        dict_ = super()._to_dict()
        if not self._apply_anchors:
            dict_.setdefault('preserved_props', []).append('line-anchors')
        # NOTE: resetting here relies on exactly one outgoing serialization per deliberate reassignment
        self._apply_anchors = False
        return dict_

    def on_anchor_change(self, handler: Handler[CodeMirrorAnchorChangeEventArguments]) -> Self:
        """Register a callback to be invoked whenever tracked anchor positions change.

        *Added in version 3.14.0*
        """
        self.on('anchor-positions', lambda e: handle_event(handler,
                CodeMirrorAnchorChangeEventArguments(sender=self, client=self.client, anchors=e.args['anchors'])))
        return self

    def _update_anchor_mirror(self, e: GenericEventArguments) -> None:
        self._anchor_positions = e.args['anchors']
