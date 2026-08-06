from typing_extensions import Self

from ... import yjs_room
from ...element import Element
from ...yjs_room import AccessCheck


class CrdtElement(Element):
    """Mixin adding ``.with_crdt(doc_id)`` for opt-in Yjs collaboration.

    Inheriting elements are responsible for the client-side Y.Doc binding
    (their Vue component reads the ``crdt-doc-id`` prop and attaches an
    appropriate plugin: ``y-codemirror.next`` for codemirror, ``y-prosemirror``
    for ProseMirror-based editors, etc.).
    """

    def with_crdt(self, doc_id: str, *, access_check: AccessCheck | None = None) -> Self:
        """Enable shared Yjs collaboration for this element.

        All elements sharing ``doc_id`` on the same NiceGUI process edit the
        same Y.Doc. Rooms live in process memory: multi-process deployments must
        route all collaborators of a ``doc_id`` to the same process (per-document
        affinity, which plain per-client sticky sessions do NOT guarantee) or
        shared state will diverge. Cross-process room sync is out of scope.

        Seed initial content via ``yjs_room.get_doc(doc_id)`` before any
        client connects. The Y.Text key the element binds to is element-specific
        (``'codemirror'`` for ``ui.codemirror``); a mismatched key or shared type
        is silently ignored rather than raised.

        Requires the ``[crdt]`` extra: ``pip install "nicegui[crdt]"``.

        :param doc_id: room name, fixed for the element's lifetime; treat as a soft secret or supply ``access_check``
        :param access_check: ``(doc_id, sid) -> bool``, sync or async; ``False`` denies joining;
            checked at join only and replacing any previously registered check for this ``doc_id``
        """
        self._props['crdt-doc-id'] = doc_id
        if access_check is not None:
            yjs_room.register_access_check(doc_id, access_check)
        else:
            yjs_room.ensure_handlers_installed()
        return self
