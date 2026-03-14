from nicegui import ui

from .. import svg

# Mascot SVG with blink animation classes on the eye paths
MASCOT_SVG = svg.HAPPY_FACE_SVG \
    .replace('class="svg_face"', 'class="svg_face" ') \
    .replace(
        'd="M14.7,38.09s3.18-2.52,6.99,0"',
        'class="svg_eye" d="M14.7,38.09s3.18-2.52,6.99,0"',
    ) \
    .replace(
        'd="M39.71,38.09s3.18-2.52,6.99,0"',
        'class="svg_eye" d="M39.71,38.09s3.18-2.52,6.99,0"',
    )


def create() -> None:
    """Create the hero section with mascot, title, CTAs, and social proof."""
    with ui.element('section').classes('mo-hero'):
        with ui.element('div').classes('mo-hero-content mo-reveal'):
            ui.html(MASCOT_SVG, sanitize=False) \
                .classes('mo-hero-mascot stroke-[#5898d4] stroke-2')

            ui.html(
                '<h1 class="mo-hero-title">Meet the <span class="mo-brand-em">NiceGUI</span>.</h1>',
                sanitize=False,
            )

            ui.html(
                '<p class="mo-hero-subtitle">'
                'Let any browser be the frontend of your Python code.'
                '</p>',
                sanitize=False,
            )

            with ui.element('div').classes('mo-cta-row'):
                ui.link('Get Started', '/#installation') \
                    .classes('mo-btn-primary').style('color: white !important')
                with ui.element('button').classes('mo-btn-install') \
                        .on('click', js_handler='''() => {
                            navigator.clipboard.writeText("pip install nicegui");
                            const toast = document.createElement("div");
                            toast.className = "mo-copy-toast";
                            toast.textContent = "ui.notify(\\'Copied!\\')";
                            document.body.appendChild(toast);
                            const rect = event.currentTarget.getBoundingClientRect();
                            toast.style.top = (rect.top - 48) + "px";
                            toast.style.left = (rect.left + rect.width / 2 - toast.offsetWidth / 2) + "px";
                            setTimeout(() => toast.remove(), 2000);
                        }'''):
                    ui.html('<code>pip install nicegui</code>', sanitize=False)
                    ui.icon('content_copy').classes('text-sm opacity-50')

            ui.html(
                '<p class="mo-social-proof">'
                '<span class="mo-social-stars">&#9733; 15,000+ GitHub stars</span>'
                ' &middot; Loved by robotics, IoT, and ML teams worldwide'
                '</p>',
                sanitize=False,
            )
