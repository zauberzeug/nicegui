import re
from html.parser import HTMLParser
from pathlib import Path

import tinycss2  # type: ignore[import-untyped]
from tinycss2.ast import AtRule, LiteralToken, Node, QualifiedRule  # type: ignore[import-untyped]

VOID_TAGS = 'area base br col embed hr img input link meta param source track wbr'.split()


class VBuild:

    def __init__(self, filepath: Path) -> None:
        parser = VueParser(filepath)
        if parser.html is None:
            raise ValueError(f'{filepath} has no template')

        name = filepath.stem.replace('/', '-').replace('\\', '-').replace(':', '-').replace('.', '-')
        html = re.sub(r'^<([\w-]+)', rf'<\1 data-{name}', parser.html)
        self.html = f'<script type="text/x-template" id="tpl-{name}">\n    {html}\n</script>'
        self.style = '\n'.join(_add_css_prefix(style, '') for style in parser.styles) + '\n'
        self.style += '\n'.join(_add_css_prefix(style, f'[data-{name}]') for style in parser.scopedStyles)
        self.script = parser.script or ''


class VueParser(HTMLParser):  # pylint: disable=abstract-method  # pylint assumes there is an abstract ``error`` method

    def __init__(self, filepath: Path):
        HTMLParser.__init__(self)
        self.rootTag: str | None = None
        self.html: str | None = None
        self.script: str | None = None
        self.styles: list[str] = []
        self.scopedStyles: list[str] = []
        self._p1: int | None = None
        self._level = 0
        self._tag = ''
        self.feed(filepath.read_text(encoding='utf-8').strip('\n\r\t '))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._tag = tag

        if tag in VOID_TAGS:
            return  # don't manage if it's a void element

        self._level += 1
        if self._level == 1 and tag == 'template':
            if self._p1 is not None:
                raise ValueError('File contains more than one template')
            self._p1 = self._get_offset() + len(self._start_tag_text)
        if self._level == 2 and self._p1:  # test p1, to be sure to be in a template
            if self.rootTag is not None:
                raise ValueError('File has more than one top level tag')
            self.rootTag = tag

    def handle_endtag(self, tag: str) -> None:
        if tag not in VOID_TAGS:
            if tag == 'template' and self._p1:  # don't watch the level (so it can accept malformed HTML)
                self.html = self.rawdata[self._p1:self._get_offset()].strip()
            self._level -= 1

    def handle_data(self, data: str) -> None:
        if self._level == 1:
            if self._tag == 'script':
                self.script = data
            if self._tag == 'style':
                if 'scoped' in self._start_tag_text.lower():
                    self.scopedStyles.append(data)
                else:
                    self.styles.append(data)

    def _get_offset(self) -> int:
        pos = 0
        for _ in range(self.lineno - 1):
            pos = self.rawdata.find('\n', pos) + 1
        return pos + self.offset

    @property
    def _start_tag_text(self) -> str:
        text = self.get_starttag_text()
        assert text is not None
        return text


def _add_css_prefix(css: str, attr: str) -> str:
    """Parse ``css`` and apply Vue-style scoped rewriting using the attribute selector ``attr``.

    ``attr`` is expected in the form ``[data-NAME]`` (or empty for non-scoped styles).
    Under scoped mode, each selector is emitted in two forms — with the attribute appended to the first compound
    (so it matches the component's root element, which carries ``data-NAME``)
    and with the classic descendant form (so it matches descendants of the root).
    At-rules are kept intact: conditional wrappers (``@media``, ``@supports``, ``@container``, ``@layer``, ``@scope``)
    have their inner rules recursed, while descriptor/keyframe blocks
    (``@keyframes``, ``@font-face``, ``@page``, ``@property``, ``@counter-style``, ``@font-feature-values``,
    ``@font-palette-values``, ``@color-profile``) are emitted verbatim.
    """
    rules = tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True)
    return '\n'.join(line for line in (_render_rule(r, attr) for r in rules) if line).strip()


def _render_rule(rule: Node, attr: str) -> str:
    if isinstance(rule, QualifiedRule):
        selectors = _split_at_top_level_comma(rule.prelude)
        if attr:
            parts: list[str] = []
            for sel in selectors:
                parts.extend(_scoped_selector_variants(_strip_scope_pseudo(sel), attr))
        else:
            parts = [_serialize_condensed(sel) for sel in selectors]
        return f'{", ".join(parts)} {{{_serialize_condensed(rule.content)} }}'
    if isinstance(rule, AtRule):
        head = f'@{rule.at_keyword}'
        if prelude := _serialize_condensed(rule.prelude):
            head += f' {prelude}'
        if rule.content is None:  # statement form, e.g. `@layer reset, theme;`
            return f'{head};'
        if rule.lower_at_keyword in {'container', 'document', 'layer', 'media', 'scope', 'starting-style', 'supports'}:
            inner_rules = tinycss2.parse_rule_list(rule.content, skip_comments=True, skip_whitespace=True)
            inner = '\n'.join(line for line in (_render_rule(r, attr) for r in inner_rules) if line)
        else:
            inner = _serialize_condensed(rule.content)  # verbatim (@keyframes, @font-face, ...)
        return f'{head} {{ {inner} }}'
    return ''  # ParseError or unexpected top-level token — skip


def _serialize_condensed(tokens: list[Node]) -> str:
    """Serialize ``tokens`` and collapse whitespace/comments to a single space."""
    text = tinycss2.serialize(tokens)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return re.sub(r'\s+', ' ', text).strip()


def _split_at_top_level_comma(tokens: list[Node]) -> list[list[Node]]:
    """Split a prelude token list at top-level commas into individual selectors."""
    groups: list[list[Node]] = [[]]
    for token in tokens:
        if isinstance(token, LiteralToken) and token.value == ',':
            groups.append([])
        else:
            groups[-1].append(token)
    return [group for group in (_trim_edge_whitespace(group) for group in groups) if group]


def _trim_edge_whitespace(tokens: list[Node]) -> list[Node]:
    start, end = 0, len(tokens)
    while start < end and tokens[start].type == 'whitespace':
        start += 1
    while end > start and tokens[end - 1].type == 'whitespace':
        end -= 1
    return tokens[start:end]


def _strip_scope_pseudo(tokens: list[Node]) -> list[Node]:
    """Remove ``:scope`` (and any whitespace right after it) so Vue's scope-root semantics apply."""
    out: list[Node] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        next_token = tokens[index + 1] if index + 1 < len(tokens) else None
        if (
            isinstance(token, LiteralToken) and
            token.value == ':' and
            next_token is not None and
            next_token.type == 'ident' and
            next_token.value == 'scope'
        ):
            index += 2
            if index < len(tokens) and tokens[index].type == 'whitespace':
                index += 1
            continue
        out.append(token)
        index += 1
    return _trim_edge_whitespace(out)


def _scoped_selector_variants(tokens: list[Node], attr: str) -> list[str]:
    """Return both rewrites for a scoped selector: ``<first-compound><attr> <rest>`` and ``*<attr> <full>``.

    The first variant covers the case where the first compound refers to the scoped root element
    itself (which carries ``data-NAME``); the second covers descendants. Within the first compound,
    the attribute is inserted before any ``::pseudo-element`` so the resulting selector stays valid.
    """
    if not tokens:
        return [attr]  # ``:scope`` alone → just the attribute selector (matches the root)

    # end of first compound: top-level whitespace or combinator
    compound_end = len(tokens)
    for index, token in enumerate(tokens):
        if token.type == 'whitespace' or (isinstance(token, LiteralToken) and token.value in {'>', '+', '~'}):
            compound_end = index
            break

    # inside the first compound, attach the attribute before any pseudo (``:hover``, ``::before``, ...)
    insert_at = compound_end
    for index in range(compound_end):
        if isinstance(tokens[index], LiteralToken) and tokens[index].value == ':':
            insert_at = index
            break

    lead_before = _serialize_condensed(tokens[:insert_at])
    lead_after = _serialize_condensed(tokens[insert_at:compound_end])
    rest = _serialize_condensed(tokens[compound_end:])
    root_form = f'{lead_before}{attr}{lead_after}' + (f' {rest}' if rest else '')
    descendant_form = f'*{attr} {_serialize_condensed(tokens)}'
    return [root_form, descendant_form]
