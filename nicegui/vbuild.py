# #############################################################################
#    Based on vbuild by manatlan (https://github.com/manatlan/vbuild)
#    Simplified and optimized for NiceGUI usage
# #############################################################################

import os
import re
from html.parser import HTMLParser

from . import optional_features

try:
    import sass
    optional_features.register('sass')
except ImportError:
    pass


class VBuildException(Exception):
    """Exception raised by VBuild operations."""
    pass


class Content:
    """Container for content with optional type information."""

    def __init__(self, value, content_type=None):
        self.type = content_type
        self.value = value.strip()

    def __repr__(self):
        return self.value


class VueParser(HTMLParser):
    """Parser to extract <template>, <script>, and <style> sections from Vue SFC files."""

    # HTML void elements that don't need closing tags
    VOID_ELEMENTS = frozenset({
        'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img',
        'input', 'keygen', 'link', 'menuitem', 'meta', 'param', 'source',
        'track', 'wbr'
    })

    def __init__(self, content, filename=''):
        super().__init__()
        self.filename = filename
        self.content = content

        # Stack-based tracking
        self._tag_stack = []
        self._current_section = None
        self._current_lang = None
        self._current_scoped = False

        # Position tracking for sections
        self._section_start = None

        # Results
        self.html = None
        self.script = None
        self.styles = []
        self.scoped_styles = []

        # Parse the content
        self.feed(content.strip())

    def handle_starttag(self, tag, attrs):
        # Parse attributes
        attributes = {k.lower(): v.lower() if v else None for k, v in attrs}
        is_scoped = 'scoped' in [k.lower() for k, v in attrs]
        lang = attributes.get('lang')

        # Check for top-level sections
        if not self._tag_stack:
            if tag == 'template':
                if self.html is not None:
                    raise VBuildException(f'Component {self.filename} contains multiple <template> tags')
                self._current_section = 'template'
                self._section_start = self.getpos()
            elif tag == 'script':
                if self.script is not None:
                    raise VBuildException(f'Component {self.filename} contains multiple <script> tags')
                self._current_section = 'script'
                self._current_lang = lang
                self._section_start = self.getpos()
            elif tag == 'style':
                self._current_section = 'style'
                self._current_lang = lang
                self._current_scoped = is_scoped
                self._section_start = self.getpos()

        # Push to stack (skip void elements)
        if tag not in self.VOID_ELEMENTS:
            self._tag_stack.append((tag, self._current_section))

    def handle_endtag(self, tag):
        if tag in self.VOID_ELEMENTS:
            return

        if not self._tag_stack:
            return

        expected_tag, section = self._tag_stack.pop()

        if tag != expected_tag:
            # This shouldn't happen with well-formed HTML, but let's be defensive
            return

        # If we're closing a top-level section, extract the content
        if not self._tag_stack and section in ['template', 'script', 'style']:
            content = self._extract_section_content(self._section_start, self.getpos())

            if section == 'template':
                self.html = Content(content)
            elif section == 'script':
                self.script = Content(content, self._current_lang)
            elif section == 'style':
                style_content = Content(content, self._current_lang)
                if self._current_scoped:
                    self.scoped_styles.append(style_content)
                else:
                    self.styles.append(style_content)

            # Reset section tracking
            self._current_section = None
            self._current_lang = None
            self._current_scoped = False
            self._section_start = None

    def _extract_section_content(self, start_pos, end_pos):
        """Extract content between start and end positions, excluding the opening tag."""
        # Find the end of the opening tag
        start_offset = self._pos_to_offset(start_pos)
        tag_end = self.content.find('>', start_offset) + 1

        # Find the start of the closing tag
        end_offset = self._pos_to_offset(end_pos)

        return self.content[tag_end:end_offset].strip()

    def _pos_to_offset(self, pos):
        """Convert line/column position to character offset."""
        line, col = pos
        offset = 0
        for _ in range(line - 1):
            offset = self.content.find('\n', offset) + 1
        return offset + col


def preprocess_css(content):
    """Apply CSS preprocessing (SCSS/SASS) to content using NiceGUI's sass integration."""
    if content.type in ['scss', 'sass']:
        if not optional_features.has('sass'):
            raise ImportError('Please run "pip install libsass" to use SASS or SCSS in Vue components.')

        # Use same approach as NiceGUI's add_scss/add_sass functions
        indented = content.type == 'sass'  # SASS uses indentation, SCSS uses braces
        return sass.compile(string=content.value.strip(), indented=indented)
    else:
        # Plain CSS or unknown type - return as-is
        return content.value


def add_css_prefix(css, prefix=''):
    """Add CSS selector prefix to all rules for scoping."""
    if not css.strip():
        return css

    # Handle @media queries
    media_blocks = []
    while '@media' in css:
        start = css.find('@media')
        brace_start = css.find('{', start) + 1

        # Find matching closing brace
        level = 1
        pos = brace_start
        while level > 0 and pos < len(css):
            if css[pos] == '{':
                level += 1
            elif css[pos] == '}':
                level -= 1
            pos += 1

        block = css[start:pos]
        media_def = block[:block.find('{')].strip()
        media_css = block[block.find('{') + 1:block.rfind('}')].strip()
        css = css.replace(block, '')
        media_blocks.append((media_def, add_css_prefix(media_css, prefix)))

    # Clean up CSS: remove comments and normalize whitespace
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    css = re.sub(r'\s+', ' ', css)

    # Process CSS rules
    lines = []
    for rule in re.findall(r'[^}]+{[^}]+}', css):
        selectors, declarations = rule.split('{', 1)

        if prefix:
            # Add prefix to each selector
            selector_list = [
                (prefix + ' ' + selector.replace(':scope', '').strip()).strip()
                for selector in selectors.split(',')
            ]
        else:
            selector_list = [selector.strip() for selector in selectors.split(',')]

        lines.append(f"{', '.join(selector_list)} {{{declarations.strip()}")

    # Add media queries back
    for media_def, media_css in media_blocks:
        lines.append(f'{media_def} {{{media_css}}}')

    return '\n'.join(lines).strip()


class VBuild:
    """
    Vue Single File Component builder for NiceGUI.

    Parses Vue SFC files and provides access to:
    - html: Template content wrapped in <script type="text/x-template">
    - script: JavaScript/TypeScript code
    - style: CSS styles (including preprocessed and scoped styles)
    """

    def __init__(self, filename, content):
        """
        Create a VBuild instance.

        Args:
            filename: Component filename (used for naming and error reporting)
            content: Vue SFC content as string
        """
        if not filename:
            raise VBuildException('Component must have a filename')

        # Extract component name from filename
        name = os.path.splitext(os.path.basename(filename))[0]

        # Create unique identifiers for this component
        unique_id = filename[:-4].replace('/', '-').replace('\\', '-').replace(':', '-').replace('.', '-')
        template_id = f'tpl-{unique_id}'
        data_id = f'data-{unique_id}'

        # Parse the Vue SFC
        parser = VueParser(content, filename)

        if parser.html is None:
            raise VBuildException(f"Component {filename} doesn't have a <template> section")

        # Add data attribute to root element for scoping
        html_content = re.sub(
            r'^<([\w-]+)',
            rf'<\1 {data_id}',
            parser.html.value
        )

        # Store component data
        self.tags = [name]
        self._html = [(template_id, html_content)]
        self._styles = []

        # Process styles
        for style in parser.styles:
            self._styles.append(('', style, filename))
        for style in parser.scoped_styles:
            self._styles.append((f'*[{data_id}]', style, filename))

        # Process script
        if parser.script:
            self._script = [parser.script.value if parser.script.value else '']
        else:
            self._script = ['']

    @property
    def html(self):
        """Return HTML template wrapped in <script type="text/x-template">."""
        templates = []
        for template_id, html_content in self._html:
            templates.append(
                f'<script type="text/x-template" id="{template_id}">{html_content}</script>'
            )
        return '\n'.join(templates)

    @property
    def script(self):
        """Return JavaScript code."""
        return '\n'.join(self._script)

    @property
    def style(self):
        """Return CSS styles (preprocessed and scoped)."""
        styles = []
        for prefix, style_content, filename in self._styles:
            try:
                processed_css = preprocess_css(style_content)
                scoped_css = add_css_prefix(processed_css, prefix)
                if scoped_css:
                    styles.append(scoped_css)
            except Exception as e:
                raise VBuildException(f'CSS preprocessing error in {filename}: {e}') from e

        return '\n'.join(styles).strip()

    def __repr__(self):
        """Return complete HTML representation of the component."""
        parts = []

        # Add styles
        if self.style:
            parts.append(f'<style>\n{self.style}\n</style>')

        # Add HTML templates
        if self.html:
            parts.append(self.html)

        # Add scripts
        if self.script:
            parts.append(f'<script>\n{self.script}\n</script>')

        return '\n'.join(parts)
