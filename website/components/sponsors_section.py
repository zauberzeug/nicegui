import json
from pathlib import Path

from nicegui import ui

from .shared import section, section_heading

SPONSORS = json.loads((Path(__file__).parent.parent / 'sponsors.json').read_text(encoding='utf-8'))


def create() -> None:
    """Create the sponsors section with logos and contributor info."""
    with section('sponsors', classes='mo-sponsors-bg'):
        section_heading('sponsors', 'Supported by the community.', center=True)

        if SPONSORS['special'] or SPONSORS['top']:
            with ui.row().classes(
                'flex gap-10 justify-center items-center flex-wrap my-10'
            ):
                for sponsor in SPONSORS['special']:
                    with ui.link(target=SPONSORS['special'][sponsor]):
                        img_path = Path(__file__).parent.parent / 'static' / 'sponsors' / f'{sponsor}.webp'
                        if img_path.exists():
                            ui.interactive_image(f'/static/sponsors/{sponsor}.webp').classes('h-12')
                        else:
                            ui.interactive_image(f'/static/sponsors/{sponsor}.light.webp') \
                                .classes('h-12 block dark:!hidden')
                            ui.interactive_image(f'/static/sponsors/{sponsor}.dark.webp') \
                                .classes('h-12 hidden dark:!block')
                for sponsor in SPONSORS['top']:
                    with ui.link(target=f'https://github.com/{sponsor}').classes('row items-center gap-2'):
                        ui.image(f'https://github.com/{sponsor}.png').classes('w-12 h-12 border')
                        ui.label(f'@{sponsor}')

            ui.markdown(f'''
                as well as {SPONSORS['normal']} other [sponsors](https://github.com/sponsors/zauberzeug)
                and {SPONSORS['contributors']} [contributors](https://github.com/zauberzeug/nicegui/graphs/contributors).
            ''').classes('text-center')
        else:
            ui.markdown(f'''
                {SPONSORS['normal']} [sponsors](https://github.com/sponsors/zauberzeug)
                and {SPONSORS['contributors']} [contributors](https://github.com/zauberzeug/nicegui/graphs/contributors).
            ''').classes('text-center')

        with ui.link(target='https://github.com/sponsors/zauberzeug').classes(
            'mo-btn-secondary inline-flex items-center gap-2 px-7 py-2.5 rounded-full'
            ' font-medium text-base cursor-pointer no-underline mx-auto mt-4 w-auto'
            ' transition-colors duration-150'
        ).style('border: 1.5px solid var(--mo-brand-blue); color: var(--mo-brand-blue)'):
            ui.icon('favorite_border').classes('text-lg')
            ui.label('Become a sponsor')
