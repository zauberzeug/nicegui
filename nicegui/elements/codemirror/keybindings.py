from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from typing_extensions import Self

from ...element import Element
from ...events import CodeMirrorKeybindingEventArguments, GenericEventArguments, Handler, handle_event


class KeybindingElement(Element):
    """Mixin mapping CodeMirror keystrokes to Python callbacks via CodeMirror's keymap.

    The frontend emits a ``keybinding`` event carrying the registered key; the registry of callbacks
    (``_keymap``) lives here on the server, while the serializable subset is mirrored into the
    ``keymap`` prop for the client to build its keymap.
    """

    def __init__(
        self,
        *,
        keymap: dict[str, Handler[CodeMirrorKeybindingEventArguments] | KeybindingElement.keybinding] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._props['keymap'] = []
        self._keymap: dict[str, KeybindingElement.keybinding] = {}
        self.on('keybinding', self._dispatch_keybinding)
        if keymap:
            with self._props.suspend_updates():
                for key, handler in keymap.items():
                    self.map_key(key, handler)

    @dataclass(frozen=True, slots=True)
    class keybinding:
        """Wraps a keybinding callback with per-key configuration overrides.

        Pass an instance as a value in the ``keymap`` mapping (or to ``map_key``) when you need to
        opt out of preventing the browser default action (e.g. "Mod-c" that notifies Python while still letting
        the browser copy normally), or to provide per-platform shortcut overrides::

            ui.codemirror(keymap={
                'Mod-c': ui.codemirror.keybinding(log_copy, prevent_default=False),
                'Alt-Down': ui.codemirror.keybinding(move_down, mac='Cmd-Down'),
            })

        Note:
            The ``key`` field on the event passed to your callback is always the
            dict key (e.g. ``'Alt-Down'``) — never the resolved per-OS variant.

        :param callback: the handler callable
        :param prevent_default: whether to mark the binding as handled (default: `True`).
            When ``True``, the browser default action is suppressed and CodeMirror stops
            keymap traversal at this binding. When ``False``, the event continues to
            lower-precedence CodeMirror bindings (e.g. ``basicSetup``'s ``Mod-z`` undo)
            *and* the browser's native handler. Use ``False`` when you want a Python
            notification without overriding either layer.
        :param mac: alternate key string used only on macOS, overriding ``key`` (default: `None`)
        :param linux: alternate key string used only on Linux, overriding ``key`` (default: `None`)
        :param win: alternate key string used only on Windows, overriding ``key`` (default: `None`)

        *Added in version 3.14.0*
        """
        callback: Handler[CodeMirrorKeybindingEventArguments]
        prevent_default: bool = field(default=True, kw_only=True)
        mac: str | None = field(default=None, kw_only=True)
        linux: str | None = field(default=None, kw_only=True)
        win: str | None = field(default=None, kw_only=True)

        def to_dict(self) -> dict[str, Any]:
            """Serialize to the frontend payload (the mapping key is added by the element)."""
            return {
                'preventDefault': self.prevent_default,
                **({'mac': self.mac} if self.mac is not None else {}),
                **({'linux': self.linux} if self.linux is not None else {}),
                **({'win': self.win} if self.win is not None else {}),
            }

    def map_key(
        self,
        key: str,
        handler: Handler[CodeMirrorKeybindingEventArguments] | KeybindingElement.keybinding,
    ) -> Self:
        """Map a keystroke to a callback.

        The ``key`` follows CodeMirror 6's keybinding syntax (e.g. "Mod-s", "F5", "Mod-Shift-d").
        "Mod" resolves to "Cmd" on macOS and "Ctrl" elsewhere.

        Pass a bare callable for the default config (prevents the browser default, no per-OS override),
        or wrap with ``keybinding`` for per-key overrides.

        Re-registering the same key replaces the prior handler. Keybindings do not fire while the editor is disabled.

        *Added in version 3.14.0*
        """
        spec = handler if isinstance(handler, KeybindingElement.keybinding) else KeybindingElement.keybinding(handler)
        self._keymap[key] = spec
        self._sync_keymap()
        return self

    def unmap_key(self, key: str) -> Self:
        """Remove a previously bound keybinding.

        No-op if the key is not currently bound.

        *Added in version 3.14.0*
        """
        if self._keymap.pop(key, None) is not None:
            self._sync_keymap()
        return self

    def _sync_keymap(self) -> None:
        self._props['keymap'] = [{'key': key, **spec.to_dict()} for key, spec in self._keymap.items()]

    def _dispatch_keybinding(self, e: GenericEventArguments) -> None:
        key = e.args['key']
        spec = self._keymap.get(key)
        if spec is None:
            return
        handle_event(spec.callback, CodeMirrorKeybindingEventArguments(sender=self, client=self.client, key=key))
