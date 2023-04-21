from nicegui import ui
from website.documentation_tools import text_demo


def main_demo() -> None:
    def ui_run_demo():
        ui.label('page with custom title')

        # ui.run(title='My App')


def more() -> None:
    @text_demo('Emoji favicon', '''
        You can use an emoji as favicon. This works in Chrome, Firefox and Safari.
    ''')
    def emoji_favicon():
        from nicegui import ui

        ui.label("NiceGUI Rocks!")

        # ui.run(favicon='🚀')

    @text_demo('Base64 favicon', '''
        You can also use an base64 encoded image as favicon.
    ''')
    def base64_favicon():
        from nicegui import ui

        ui.label("NiceGUI with a dot!")

        icon = 'data:image/png;base64,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'
        # ui.run(favicon=icon)

    @text_demo('SVG favicon', '''
        And directly use an svg as favicon. Works in Chrome, Firefox and Safari.
    ''')
    def svg_favicon():
        from nicegui import ui

        ui.label("NiceGUI makes you smile!")

        smiley = '''
            <svg viewBox="0 0 200 200" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="78" fill="#ffde34" stroke="black" stroke-width="3" />
            <circle cx="80" cy="85" r="8" />
            <circle cx="120" cy="85" r="8" />
            <path d="m60,120 C75,150 125,150 140,120" style="fill:none; stroke:black; stroke-width:8; stroke-linecap:round" />
            </svg>'''
        # ui.run(favicon=smiley)
