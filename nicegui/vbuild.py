import re
from html.parser import HTMLParser
from pathlib import Path

VOID_TAGS = 'area base br col embed hr img input link meta param source track wbr'.split()


class VBuild:

    def __init__(self, filepath: Path) -> None:
        parser = VueParser(filepath)
        if parser.html is None:
            raise ValueError(f'{filepath} has no template')

        name = filepath.stem.replace('/', '-').replace('\\', '-').replace(':', '-').replace('.', '-')
        html = re.sub(r'^<([\w-]+)', rf'<\1 data-{name}', parser.html)
        self.html = f'<script type="text/x-template" id="tpl-{name}">\n    {html}\n</script>'
        self.style = '\n'.join(add_css_prefix(style, '') for style in parser.styles) + '\n'
        self.style += '\n'.join(add_css_prefix(style, f'*[data-{name}]') for style in parser.scopedStyles)
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


def add_css_prefix(css: str, prefix: str) -> str:
    """Add the prefix (CSS selector) to all rules in ``css``."""
    media_queries: list[tuple[str, str]] = []
    while '@media' in css:
        p1 = css.find('@media', 0)
        p2 = css.find('{', p1) + 1
        level = 1
        while level > 0:
            level += 1 if css[p2] == '{' else -1 if css[p2] == '}' else 0
            p2 += 1
        block = css[p1:p2]
        media_def = block[:block.find('{')].strip()
        media_css = block[block.find('{') + 1:block.rfind('}')].strip()
        css = css.replace(block, '')
        media_queries.append((media_def, add_css_prefix(media_css, prefix)))

    lines: list[str] = []
    css = re.sub(re.compile(r'/\*.*?\*/', re.DOTALL), '', css)
    css = re.sub(re.compile(r'[ \t\n]+', re.DOTALL), ' ', css)
    for rule in re.findall(r'[^}]+{[^}]+}', css):
        selectors, declarations = rule.split('{', 1)
        if prefix:
            line = [(prefix + ' ' + i.replace(':scope', '').strip()).strip() for i in selectors.split(',')]
        else:
            line = [i.strip() for i in selectors.split(',')]
        lines.append(', '.join(line) + ' {' + declarations.strip())
    lines.extend(f'{d} {{ {c} }}' for d, c in media_queries)
    return '\n'.join(lines).strip()
