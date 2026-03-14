from nicegui import ui

from ..style import link_target


def create() -> None:
    """Create the Why section with pull-quote, timeline, and tech stack."""
    with ui.element('section').classes('mo-why-section').props('id=why'):
        link_target('why', '70px')
        with ui.element('div').classes('mo-why-inner mo-reveal'):
            ui.html('<div class="mo-section-label">why</div>', sanitize=False)
            ui.html('<h2 class="mo-section-title">Why?</h2>', sanitize=False)

            ui.html(
                '<blockquote class="mo-why-pullquote">'
                '&ldquo;We liked Streamlit but found it does too much magic '
                'when it comes to state handling.&rdquo;'
                '</blockquote>',
                sanitize=False,
            )

            with ui.element('div').classes('mo-why-timeline'):
                # Streamlit
                with ui.element('div').classes('mo-why-timeline-step'):
                    ui.element('div').classes('mo-why-timeline-dot')
                    ui.html('<strong>Streamlit</strong>', sanitize=False)
                    ui.html(
                        '<span class="mo-why-timeline-desc">'
                        'Great for quick dashboards, but implicit re-runs make complex state tricky.'
                        '</span>',
                        sanitize=False,
                    )

                ui.element('div').classes('mo-why-timeline-connector')

                # JustPy
                with ui.element('div').classes('mo-why-timeline-step'):
                    ui.element('div').classes('mo-why-timeline-dot')
                    ui.html('<strong>JustPy</strong>', sanitize=False)
                    ui.html(
                        '<span class="mo-why-timeline-desc">'
                        'Right idea — components in Python — but too bare-bones for production UIs.'
                        '</span>',
                        sanitize=False,
                    )

                ui.element('div').classes('mo-why-timeline-connector')

                # NiceGUI (active)
                with ui.element('div').classes('mo-why-timeline-step mo-why-timeline-step-active'):
                    ui.element('div').classes('mo-why-timeline-dot')
                    ui.html('<strong>NiceGUI</strong>', sanitize=False)
                    ui.html(
                        '<span class="mo-why-timeline-desc">'
                        'Explicit state, rich components, and batteries included — the sweet spot.'
                        '</span>',
                        sanitize=False,
                    )

            ui.html(
                '<p class="mo-why-techstack">'
                'Built with <a href="https://vuejs.org/">Vue</a> and '
                '<a href="https://quasar.dev/">Quasar</a> on the frontend, '
                '<a href="https://fastapi.tiangolo.com/">FastAPI</a>, '
                '<a href="https://www.starlette.io/">Starlette</a>, and '
                '<a href="https://www.uvicorn.org/">Uvicorn</a> under the hood.'
                '</p>',
                sanitize=False,
            )
