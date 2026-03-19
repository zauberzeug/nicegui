from nicegui import ui

from .. import svg
from .shared import cta_button


def create() -> None:
    """Create the hero section with mascot, title, CTAs, and social proof."""
    with ui.element('section').classes(
        'min-h-screen flex flex-col items-center justify-center text-center px-6 pb-20 relative overflow-hidden w-full bg-(--mo-bg)'
    ):
        ui.element().classes('absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1400px] h-[1000px] pointer-events-none') \
            .style('background:'
                   ' radial-gradient(ellipse at 40% 45%, color-mix(in srgb, var(--mo-brand-blue) 7%, transparent) 0%, transparent 55%),'
                   ' radial-gradient(ellipse at 60% 55%, color-mix(in srgb, var(--mo-brand-blue-light) 4%, transparent) 0%, transparent 50%),'
                   ' radial-gradient(ellipse at 50% 50%, var(--mo-warm-glow) 0%, transparent 65%)')
        with ui.column().classes('mo-reveal relative max-w-[800px] flex flex-col items-center gap-6'):
            ui.html(svg.HAPPY_FACE_SVG, sanitize=False) \
                .classes('mo-hero-mascot size-40 stroke-[#5898d4] stroke-2 mb-6')
            ui.markdown('Meet the *NiceGUI*.') \
                .classes('text-[clamp(2.5rem,5vw,4.5rem)] font-semibold tracking-tighter leading-none fancy-em text-(--mo-text-primary)')
            ui.label('Let any browser be the frontend of your Python code.') \
                .classes('text-xl max-w-[560px] leading-relaxed text-(--mo-text-secondary)')

            with ui.row(align_items='center').classes('gap-4 justify-center mt-2'):
                cta_button('Get Started', right_icon='ph-arrow-right',
                           on_click=lambda: ui.navigate.to('/#installation'))
                cta_button('pip install nicegui', right_icon='ph-copy', filled=False, blue=False, mono=True,
                           on_click=lambda: ui.notify('Copied!', color='primary'))

            with ui.row().classes('text-sm text-(--mo-text-muted) gap-2'):
                ui.html('&#9733; 15,000+ GitHub stars').classes('text-(--mo-warm-accent)')
                ui.html('&middot;')
                ui.label('Loved by robotics, IoT, and ML teams worldwide')
