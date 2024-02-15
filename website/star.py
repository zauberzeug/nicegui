from nicegui import ui
from nicegui.element import Element
from website import svg

STYLE = '''
<style>
    @keyframes star-tumble {
          0% { transform: translateX(6em) rotate(432deg); }
        100% { transform: translateX(0)   rotate(0);      }
    }
    @keyframes star-pulse {
          0% { scale: 1.0; }
         60% { scale: 1.0; }
         70% { scale: 1.2; }
         80% { scale: 1.0; }
         90% { scale: 1.2; }
        100% { scale: 1.0; }
    }
    .star {
        height: 1.75em;
        fill: white;
        animation: 1s ease-in-out 6s both star-tumble,
                   3s ease-in-out 3s infinite star-pulse;
    }
    .star:hover {
        fill: rgb(250 204 21);
    }

    @keyframes star-grow {
          0% { width: 0 }
        100% { width: 2em }
    }
    .star-container {
        animation: 1s ease-in-out 6s both star-grow;
    }
</style>
'''

STAR = '''
<svg viewBox="0 0 16 16">
    <path d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25zm0 2.445L6.615 5.5a.75.75 0 01-.564.41l-3.097.45 2.24 2.184a.75.75 0 01.216.664l-.528 3.084 2.769-1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 0 01.216-.664l2.24-2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z"></path>
</svg>
'''


def add_star() -> ui.link:
    """
    Adds a star container with a link to the NiceGUI GitHub repository.

    This function creates a star container element with a link to the NiceGUI GitHub repository.
    It also includes a tooltip with a message encouraging users to star the repository and
    spread the word about NiceGUI.

    Returns:
        ui.link: The star container element with the link to the GitHub repository.
    """
    ui.add_head_html(STYLE)
    with ui.link(target='https://github.com/zauberzeug/nicegui/').classes('star-container') as link:
        with Element('svg').props('viewBox="0 0 24 24"').classes('star'):
            Element('path').props('d="M23.555,8.729a1.505,1.505,0,0,0-1.406-.98H16.062a.5.5,0,0,1-.472-.334L13.405,1.222a1.5,1.5,0,0,0-2.81,0l-.005.016L8.41,7.415a.5.5,0,0,1-.471.334H1.85A1.5,1.5,0,0,0,.887,10.4l5.184,4.3a.5.5,0,0,1,.155.543L4.048,21.774a1.5,1.5,0,0,0,2.31,1.684l5.346-3.92a.5.5,0,0,1,.591,0l5.344,3.919a1.5,1.5,0,0,0,2.312-1.683l-2.178-6.535a.5.5,0,0,1,.155-.543l5.194-4.306A1.5,1.5,0,0,0,23.555,8.729Z"')
        with ui.tooltip('').classes('bg-[#486991] w-96 p-4'):
            with ui.row().classes('items-center no-wrap'):
                svg.face().classes('w-14 stroke-white stroke-[1pt]')
                with ui.column().classes('p-2 gap-2'):
                    ui.label('Star us on GitHub!').classes('text-[180%]')
                    ui.label('And tell others about NiceGUI.').classes('text-[140%]')
    return link
