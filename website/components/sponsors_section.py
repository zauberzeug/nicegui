import json
from pathlib import Path

from nicegui import ui

from .. import design as d
from ..utils import themed_image
from .shared import cta_button, section, section_heading

SPONSORS = json.loads((Path(__file__).parent.parent / 'sponsors.json').read_text(encoding='utf-8'))


def create() -> None:
    """Create the sponsors section with logos and contributor info."""
    with section('sponsors', classes=d.BG_SPONSORS):
        section_heading('sponsors', 'Supported by the community.', center=True)

        if SPONSORS['special'] or SPONSORS['top']:
            with ui.row().classes('gap-10 justify-center items-center my-10 w-full'):
                for sponsor in SPONSORS['special']:
                    with ui.link(target=SPONSORS['special'][sponsor]):
                        img_path = Path(__file__).parent.parent / 'static' / 'sponsors' / f'{sponsor}.webp'
                        if img_path.exists():
                            ui.interactive_image(f'/static/sponsors/{sponsor}.webp').classes('h-12')
                        else:
                            themed_image(f'/static/sponsors/{sponsor}.THEME.webp', classes='h-12')
                for sponsor in SPONSORS['top']:
                    with ui.link(target=f'https://github.com/{sponsor}').classes('row items-center gap-2'):
                        ui.image(f'https://github.com/{sponsor}.png').classes('size-12 border')
                        ui.label(f'@{sponsor}')

            ui.markdown(f'''
                as well as {SPONSORS['normal']} other [sponsors](https://github.com/sponsors/zauberzeug)
                and {SPONSORS['contributors']} [contributors](https://github.com/zauberzeug/nicegui/graphs/contributors).
            ''').classes('w-full text-center')
        else:
            ui.markdown(f'''
                {SPONSORS['normal']} [sponsors](https://github.com/sponsors/zauberzeug)
                and {SPONSORS['contributors']} [contributors](https://github.com/zauberzeug/nicegui/graphs/contributors).
            ''').classes('w-full text-center')

        cta_button('Become a sponsor', left_icon='ph-heart', filled=False,
                   on_click=lambda: ui.navigate.to('https://github.com/sponsors/zauberzeug')) \
            .classes('mx-auto mt-4')
