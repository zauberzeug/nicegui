from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from typing_extensions import Self

from ...element import Element
from ...events import CodeMirrorKeybindingEventArguments, GenericEventArguments, Handler, handle_event


class KeybindingElement(Element):
    """Mixin mapping CodeMirror keystrokes to Python callbacks via CodeMirror's keymap.

    The frontend emits a ``keybinding`` event carrying the registered key; the registry of callbacks
    (``_keybinding_specs``) lives here on the server, while the serializable subset is mirrored into the
    ``keybindings`` prop for the client to build its keymap.
    """

    def __init__(
        self,
        *,
        keybindings: dict[str, Handler[CodeMirrorKeybindingEventArguments] | KeybindingElement.binding] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._props['keybindings'] = []
        self._keybinding_specs: dict[str, KeybindingElement.binding] = {}
        self.on('keybinding', self._dispatch_keybinding)
        if keybindings:
            with self._props.suspend_updates():
                for key, handler in keybindings.items():
                    self.on_keybinding(key, handler)

    @dataclass(frozen=True, slots=True)
    class binding:
        """Wraps a keybinding callback with per-binding configuration overrides.

        Pass an instance as a value in the ``keybindings`` mapping (or to ``on_keybinding``) when you need to
        opt out of preventing the browser default action (e.g. "Mod-c" that notifies Python while still letting
        the browser copy normally), or to provide per-platform shortcut overrides::

            ui.codemirror(keybindings={
                'Mod-c': ui.codemirror.binding(log_copy, prevent_default=False),
                'Alt-Down': ui.codemirror.binding(move_down, mac='Cmd-Down'),
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

    def on_keybinding(
        self,
        key: str,
        handler: Handler[CodeMirrorKeybindingEventArguments] | KeybindingElement.binding,
    ) -> Self:
        """Bind a keystroke to a callback.

        The ``key`` follows CodeMirror 6's keybinding syntax (e.g. "Mod-s", "F5", "Mod-Shift-d").
        "Mod" resolves to "Cmd" on macOS and "Ctrl" elsewhere.

        Pass a bare callable for the default config (prevents the browser default, no per-OS override),
        or wrap with ``binding`` for per-binding overrides.

        Re-registering the same key replaces the prior handler. Bindings do not fire while the editor is disabled.

        *Added in version 3.14.0*
        """
        spec = handler if isinstance(handler, KeybindingElement.binding) else KeybindingElement.binding(handler)
        self._keybinding_specs[key] = spec
        self._sync_keybindings_prop()
        return self

    def remove_keybinding(self, key: str) -> Self:
        """Remove a previously bound keybinding.

        No-op if the key is not currently bound.

        *Added in version 3.14.0*
        """
        if self._keybinding_specs.pop(key, None) is not None:
            self._sync_keybindings_prop()
        return self

    def _sync_keybindings_prop(self) -> None:
        self._props['keybindings'] = [{'key': key, **spec.to_dict()} for key, spec in self._keybinding_specs.items()]

    def _dispatch_keybinding(self, e: GenericEventArguments) -> None:
        key = e.args['key']
        spec = self._keybinding_specs.get(key)
        if spec is None:
            return
        handle_event(spec.callback, CodeMirrorKeybindingEventArguments(sender=self, client=self.client, key=key))
