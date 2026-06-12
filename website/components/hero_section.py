from nicegui import ui

from .. import design as d
from .. import svg
from .shared import cta_button


def create() -> None:
    """Create the hero section with mascot, title, CTAs, and social proof."""
    with ui.element('section').classes(
        f'-mt-16 pt-24 min-h-screen flex flex-col items-center justify-center text-center px-6 pb-20 relative overflow-hidden w-full {d.BG}'
    ):
        ui.element().classes(
            f'absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1400px] h-[1000px] pointer-events-none '
            f'bg-[radial-gradient(ellipse_at_50%_48%,color-mix(in_srgb,{d.BLUE}_10%,transparent)_0%,transparent_60%)]'
        )
        with ui.column(align_items='center').classes('reveal'):
            ui.html(svg.HAPPY_FACE_SVG, sanitize=False) \
                .classes(f'hero-mascot size-40 stroke-[{d.BLUE}] stroke-2 mb-8')
            ui.markdown('Meet the *NiceGUI*.') \
                .classes(f'{d.TEXT_HERO} font-semibold tracking-tighter leading-none [&_em]:not-italic [&_em]:{d.TEXT_BLUE} {d.TEXT_PRIMARY} -mb-2')
            ui.markdown('''
                Let any browser be the frontend of your Python code.<br>
                Loved by robotics, IoT, and ML teams worldwide.
            ''').classes(f'{d.TEXT_19PX} leading-relaxed {d.TEXT_SECONDARY}')

            with ui.row(align_items='center').classes('gap-4 justify-center mt-2'):
                cta_button('Get Started', right_icon='ph-arrow-right') \
                    .on_click(lambda: ui.navigate.to('/#installation'))
                cta_button('pip install nicegui', right_icon='ph-copy', filled=False, blue=False, mono=True) \
                    .on_click(lambda: ui.clipboard.write('pip install nicegui')) \
                    .on_click(lambda: ui.notify('Copied!', color='primary'))
