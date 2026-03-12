from nicegui import ui
from nicegui.elements.restructured_text import prepare_content


class CustomRestructuredText(ui.restructured_text):
    """Custom restructured text element that avoids field lists being interpreted as document-level fields (see #4647)."""

    def _handle_content_change(self, content: str) -> None:
        html = prepare_content('__PLACEHOLDER__\n\n' + content).replace('<p>__PLACEHOLDER__</p>\n', '')
        if self._props.get('innerHTML') != html:
            self._props['innerHTML'] = html
