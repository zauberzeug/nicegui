from nicegui import ui

from .. import svg

MASCOT_SVG = svg.HAPPY_FACE_SVG

PIP_COPY_JS = '''() => {
    navigator.clipboard.writeText("pip install nicegui");
    const toast = document.createElement("div");
    toast.className = "mo-copy-toast";
    toast.textContent = "ui.notify('Copied!')";
    document.body.appendChild(toast);
    const rect = event.currentTarget.getBoundingClientRect();
    toast.style.top = (rect.top - 48) + "px";
    toast.style.left = (rect.left + rect.width / 2 - toast.offsetWidth / 2) + "px";
    setTimeout(() => toast.remove(), 2000);
}'''


def create() -> None:
    """Create the hero section with mascot, title, CTAs, and social proof."""
    with ui.element('section').classes('mo-hero'):
        with ui.column().classes('mo-hero-content mo-reveal'):
            ui.html(MASCOT_SVG, sanitize=False).classes('mo-hero-mascot stroke-[#5898d4] stroke-2')
            ui.markdown('Meet the *NiceGUI*.').classes('mo-hero-title fancy-em')
            ui.label('Let any browser be the frontend of your Python code.').classes('mo-hero-subtitle')

            with ui.row().classes('mo-cta-row'):
                with ui.link(target='/#installation').classes('mo-btn-primary'):
                    ui.label('Get Started')
                    ui.html('''<svg width="16" height="16" viewBox="0 0 16 16" fill="none"
                               stroke="currentColor" stroke-width="2">
                               <path d="M3 8h10m-4-4l4 4-4 4" /></svg>''', sanitize=False)
                with ui.element('button').classes('mo-btn-install').on('click', js_handler=PIP_COPY_JS):
                    ui.html('<code>pip install nicegui</code>', sanitize=False)
                    ui.icon('content_copy').classes('text-sm opacity-50')

            ui.html('''<p class="mo-social-proof">
                <span class="mo-social-stars">&#9733; 15,000+ GitHub stars</span>
                &middot; Loved by robotics, IoT, and ML teams worldwide
            </p>''', sanitize=False)
