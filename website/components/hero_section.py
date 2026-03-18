from nicegui import ui

from .. import svg


def create() -> None:
    """Create the hero section with mascot, title, CTAs, and social proof."""
    with ui.element('section').classes(
        'mo-hero min-h-screen flex flex-col items-center justify-center text-center'
        ' px-6 pb-20 relative overflow-hidden w-full bg-(--mo-bg)'
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

            with ui.row().classes('mo-cta-row flex gap-4 items-center flex-wrap justify-center mt-2'):
                with ui.link(target='/#installation').classes(
                    'mo-btn-primary inline-flex items-center gap-2 px-7 py-3 rounded-full'
                    ' font-medium text-base cursor-pointer no-underline w-auto'
                    ' transition-all duration-150 hover:-translate-y-px'
                    ' bg-(--mo-brand-blue) text-white'
                ).style('box-shadow: 0 2px 8px color-mix(in srgb, var(--mo-brand-blue) 30%, transparent)'):
                    ui.label('Get Started')
                    ui.html('''
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M3 8h10m-4-4l4 4-4 4" />
                        </svg>
                    ''', sanitize=False)
                pip_btn = ui.element('button').classes(
                    'inline-flex items-center gap-2 px-6 py-3 rounded-full font-mono text-sm'
                    ' cursor-pointer transition-colors duration-150 w-auto text-(--mo-text-primary)'
                ).style('border: 1.5px solid var(--mo-border); background: transparent')
                pip_btn.on('click', lambda: ui.notify('Copied!', color='primary'))
                with pip_btn:
                    ui.html('<code>pip install nicegui</code>', sanitize=False)
                    ui.icon('content_copy').classes('text-sm opacity-50')

            ui.html('''<p style="font-size: 0.875rem; color: var(--mo-text-muted)">
                <span style="color: var(--mo-warm-accent)">&#9733; 15,000+ GitHub stars</span>
                &middot; Loved by robotics, IoT, and ML teams worldwide
            </p>''', sanitize=False)
