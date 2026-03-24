import json
from pathlib import Path

from nicegui import ui

from .. import design as d
from ..design import phosphor_icon, themed_image
from ..github_stars import stars
from .shared import cta_button, section, section_heading

SPONSORS = json.loads((Path(__file__).parent.parent / 'sponsors.json').read_text(encoding='utf-8'))


def create() -> None:
    """Create the sponsors section with logos and contributor info."""
    with section('sponsors'), ui.column().classes(f'reveal w-full {d.BG_BLUE}/25 rounded-xl py-16 {d.SHADOW_CARD}'):
        section_heading('sponsors', 'Supported by the community.', center=True)

        ui.label('Join thousands of developers building with NiceGUI!') \
            .classes(f'self-center text-center {d.TEXT_SECONDARY}')

        with ui.row(align_items='center').classes('gap-12 justify-center my-10 w-full'):
            _fact('ph-star', stars.string, 'GitHub Stars')
            _fact('ph-github-logo', str(SPONSORS['contributors']), 'Contributors')
            _fact('ph-heart', str(SPONSORS['total']), 'Sponsors')

        with ui.row(align_items='center').classes('gap-10 justify-center my-5 w-full'):
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

            cta_button('Become a sponsor', left_icon='ph-heart', filled=False,
                       on_click=lambda: ui.navigate.to('https://github.com/sponsors/zauberzeug')) \
                .classes(f'{d.BORDER_ACCENT} [&_.ph-heart]:{d.TEXT_ACCENT}')


def _fact(icon: str, number: str, label: str) -> None:
    with ui.column(align_items='center').classes('gap-0'):
        phosphor_icon(icon).classes(f'{d.TEXT_32PX} {d.TEXT_ACCENT}')
        ui.label(number).classes(d.TEXT_24PX)
        ui.label(label).classes(f'{d.TEXT_13PX} {d.TEXT_SECONDARY}')
