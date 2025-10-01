from nicegui import ui

from . import doc

doc.title('ui.*run*')


@doc.demo(ui.run, tab='My App')
def demo() -> None:
    ui.label('page with custom title')

    # ui.run(title='My App')


@doc.demo('Emoji favicon', '''
    You can use an emoji as favicon.
    This works in Chrome, Firefox and Safari.
''', tab=lambda: ui.markdown('🚀&nbsp; NiceGUI'))
def emoji_favicon():
    ui.label('NiceGUI rocks!')

    # ui.run(favicon='🚀')


@doc.demo(
    'Base64 favicon', '''
    You can also use an base64-encoded image as favicon.
''', tab=lambda: (
        ui.image('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==')
        .classes('w-4 h-4'),
        ui.label('NiceGUI'),
    ),
)
def base64_favicon():
    ui.label('NiceGUI with a red dot!')

    icon = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='

    # ui.run(favicon=icon)


@doc.demo('SVG favicon', '''
    And directly use an SVG as favicon.
    Works in Chrome, Firefox and Safari.
''', tab=lambda: (
    ui.html('''
        <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="78" fill="#ffde34" stroke="black" stroke-width="3" />
            <circle cx="80" cy="85" r="8" />
            <circle cx="120" cy="85" r="8" />
            <path d="m60,120 C75,150 125,150 140,120" style="fill:none; stroke:black; stroke-width:8; stroke-linecap:round" />
        </svg>
    ''', sanitize=False).classes('w-4 h-4'),
    ui.label('NiceGUI'),
))
def svg_favicon():
    ui.label('NiceGUI makes you smile!')

    smiley = '''
        <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="78" fill="#ffde34" stroke="black" stroke-width="3" />
            <circle cx="80" cy="85" r="8" />
            <circle cx="120" cy="85" r="8" />
            <path d="m60,120 C75,150 125,150 140,120" style="fill:none; stroke:black; stroke-width:8; stroke-linecap:round" />
        </svg>
    '''

    # ui.run(favicon=smiley)


@doc.demo('Custom welcome message', '''
    You can mute the default welcome message on the command line setting the `show_welcome_message` to `False`.
    Instead you can print your own welcome message with a custom startup handler.
''')
def custom_welcome_message():
    from nicegui import app

    ui.label('App with custom welcome message')
    #
    # app.on_startup(lambda: print('Visit your app on one of these URLs:', app.urls))
    #
    # ui.run(show_welcome_message=False)
