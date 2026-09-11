from __future__ import annotations

from typing import Any, Literal, TypedDict, cast

from typing_extensions import NotRequired

from ...element import Element
from ...logging import log

# Functional TypedDict syntax because `from` and `class` are Python keywords.
MarkDecorationSpec = TypedDict(
    'MarkDecorationSpec',
    {
        'kind': Literal['mark'],
        'from': int,
        'to': int,
        'class': NotRequired[str],
        'attributes': NotRequired[dict[str, str]],
        'inclusiveStart': NotRequired[bool],
        'inclusiveEnd': NotRequired[bool],
    },
)

LineDecorationSpec = TypedDict(
    'LineDecorationSpec',
    {
        'kind': Literal['line'],
        'line': int,
        'class': NotRequired[str],
        'attributes': NotRequired[dict[str, str]],
    },
)

ReplaceDecorationSpec = TypedDict(
    'ReplaceDecorationSpec',
    {
        'kind': Literal['replace'],
        'from': int,
        'to': int,
        'text': NotRequired[str],
        'class': NotRequired[str],
        'inclusive': NotRequired[bool],
        'block': NotRequired[bool],
    },
)

WidgetDecorationSpec = TypedDict(
    'WidgetDecorationSpec',
    {
        'kind': Literal['widget'],
        'position': int,
        'text': str,
        'class': NotRequired[str],
        'side': NotRequired[Literal[-1, 1]],
    },
)

DecorationSpec = MarkDecorationSpec | LineDecorationSpec | ReplaceDecorationSpec | WidgetDecorationSpec

# The keys a spec must carry per kind, and the lower bound of every numeric field.
_DECORATION_REQUIRED: dict[str, tuple[str, ...]] = {
    'mark': ('from', 'to'),
    'line': ('line',),
    'replace': ('from', 'to'),
    'widget': ('position', 'text'),
}
_DECORATION_MINIMUMS: dict[str, int] = {'from': 0, 'to': 0, 'position': 0, 'line': 1}


class DecorationElement(Element):
    """Mixin applying CodeMirror decorations declared as a list of specs.

    Unlike line anchors, the browser reports nothing back: CodeMirror keeps each decoration pinned
    to its text as the document changes, but the "decorations" prop holds the specs as declared.
    A deliberate write, an assignment as well as an in-place change of the list, sends them and
    re-applies every spec at its declared offset; on unrelated updates the prop is preserved,
    so the client keeps the positions it has mapped.
    """

    def __init__(
        self,
        *,
        decorations: list[DecorationSpec] | None = None,
        decoration_text_html: bool = False,
        **kwargs: Any,
    ) -> None:
        # NOTE: validate before super().__init__ registers the element, so a rejected argument
        # does not leave a half-built element behind in the element tree
        _validate_decorations(decorations or [])
        super().__init__(**kwargs)
        self._props['decorations'] = decorations or []
        self._decorations_pending = True
        # The list stays the same object for the element's lifetime (the setter fills it in place),
        # so a reference a caller kept stays live and the change handler is registered exactly once.
        self._props['decorations'].on_change(self._mark_decorations_pending)
        self._props['decoration-text-html'] = decoration_text_html

    @property
    def decorations(self) -> list[DecorationSpec]:
        """Decoration specs applied to the editor; mutating this list syncs to the client.

        Decorations style or modify the editor's rendering without changing the underlying document.
        Each entry is a ``MarkDecorationSpec``, ``LineDecorationSpec``, ``ReplaceDecorationSpec``
        or ``WidgetDecorationSpec`` dict.
        The ``class`` field styles a mark or line, or the ``text`` a replace or widget decoration shows;
        a replace decoration without ``text`` renders nothing that could carry it.
        The host application is responsible for shipping CSS for whatever class names it passes here.
        The ``attributes`` field is applied as raw DOM attributes (including event handlers like
        ``onclick``) and is not sanitized.
        Do not pass untrusted input through it.

        The ``from``, ``to`` and ``position`` fields are Python ``str`` indices into ``value``,
        so ``value.index(...)`` addresses what you expect even in a document containing emoji.
        A widget's ``side`` (default ``1``) places it after ``position``, so text typed exactly there
        lands before the widget; ``-1`` places it before, so typed text lands after it.

        The browser keeps decorations pinned to their text as the document changes, but unlike
        ``line_anchors`` it does not report the moved positions back: reading this property returns
        the specs as declared, and a fresh client (a second browser on a shared page, say) receives
        those declared offsets against whatever ``value`` is by then.
        Every write, an assignment as well as an in-place change of the list, applies all specs afresh
        at their declared offsets, so compute them from the current ``value``, and prefer assigning
        a complete list over appending to one whose other entries the user may have typed past.

        A spec that cannot describe a decoration at all (an unknown kind, a missing required key,
        an inverted or negative offset, an empty mark range) is rejected with a ``ValueError`` on assignment;
        one that slips in through an in-place change is skipped with a warning when it is sent.
        Whether it fits the document is decided in the browser, which warns and skips just that spec.

        *Added in version 3.17.0*
        """
        return self._props['decorations']

    @decorations.setter
    def decorations(self, decorations: list[DecorationSpec] | None) -> None:
        decorations = decorations or []
        _validate_decorations(decorations)
        self._props['decorations'][:] = decorations

    def _mark_decorations_pending(self) -> None:
        self._decorations_pending = True

    def _to_dict(self) -> dict[str, Any]:
        dict_ = super()._to_dict()
        # An in-place change bypasses the setter, so the specs are checked once more on the way out.
        # The filter runs on every send, since a full render (a new client of a shared page, or a
        # re-render after a listener change) uses these props verbatim; the warning is logged only
        # once, when the write that let the spec in is flushed.
        usable: list[DecorationSpec] = []
        for spec in self._props['decorations']:
            error = _decoration_error(spec)
            if error is None:
                usable.append(spec)
            elif self._decorations_pending:
                log.warning(f'{error}; skipping it')
        dict_['props'] = {**dict_['props'], 'decorations': usable}
        if not self._decorations_pending:
            # An unrelated update must leave the positions the browser has mapped alone, as with line anchors.
            dict_.setdefault('preserved_props', []).append('decorations')
        self._decorations_pending = False
        return dict_


def _decoration_error(entry: DecorationSpec) -> str | None:
    """Explain why a spec cannot describe a decoration, whatever the document says, or return ``None``.

    Everything document-dependent (offsets past the end, empty replace ranges, lines that do not
    exist) stays on the JS side, which warns and skips the individual spec.
    """
    spec = cast('dict[str, Any]', entry)  # the TypedDicts describe intent; at runtime this is user data
    kind = spec.get('kind')
    if kind not in _DECORATION_REQUIRED:
        return f'decorations: unknown kind {kind!r}, expected one of {", ".join(sorted(_DECORATION_REQUIRED))}'
    for key in _DECORATION_REQUIRED[kind]:
        if key not in spec:
            return f'decorations: {kind} decoration is missing required key {key!r}'
    for key, minimum in _DECORATION_MINIMUMS.items():
        if key not in spec:
            continue
        value = spec[key]
        if not isinstance(value, int) or isinstance(value, bool):
            return f'decorations: {kind} decoration needs an integer {key!r} (got {value!r})'
        if value < minimum:
            bound = 'lines are 1-indexed' if key == 'line' else 'offsets start at 0'
            return f'decorations: {kind} decoration has {key}={value}, but {bound}'
    if kind in ('mark', 'replace') and spec['from'] > spec['to']:
        return f'decorations: {kind} decoration has from={spec["from"]} > to={spec["to"]}'
    if kind == 'mark' and spec['from'] == spec['to']:
        return f'decorations: mark decoration has from=to={spec["from"]}, but a mark needs a non-empty range'
    if 'text' in spec and not isinstance(spec['text'], str):
        return f'decorations: {kind} decoration needs a string \'text\' (got {spec["text"]!r})'
    return None


def _validate_decorations(decorations: list[DecorationSpec]) -> None:
    for spec in decorations:
        error = _decoration_error(spec)
        if error is not None:
            raise ValueError(error)
