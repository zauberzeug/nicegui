from nicegui import ui
from pathlib import Path

css_file = Path(__file__).parent / "fontColor.css"
css_txt = f"""<style>{css_file.read_text()}</style>"""

class FontColor(ui.element):
    def __init__(self,) -> None:
        super().__init__("div")
        self.props("data-v-09ce85c6")
        ui.add_head_html(css_txt)
