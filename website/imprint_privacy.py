from nicegui import ui

from . import design as d
from .components.shared import section


def create() -> None:
    ui.page_title('Imprint & Privacy | NiceGUI')

    with section('imprint', classes='py-32!'):
        ui.link_target('imprint')
        _heading('Imprint')

        _subheading('Zauberzeug GmbH')
        _text('''
            Hohenholter Str. 43, 48329 Havixbeck, Germany

            Represented by Rodion (Rodja) Trappe

            Phone: +49 2507 3817, Email: info@zauberzeug.com
        ''')

        _subheading('Registry entry')
        _text('Registry court: Amtsgericht Coesfeld, Registry number: HRB 14215')

        _subheading('Tax')
        _text('Sales tax identification number according to §27a Sales Tax Act: DE286384205')

        ui.link_target('privacy')
        _heading('Privacy Policy')
        _text('''
            We use [Plausible Analytics](https://plausible.io) to understand how you interact with our site.
            Plausible Analytics is a privacy-first analytics tool
            that does not use cookies or collect any personal data or personally identifiable information (PII).
            All data collected by Plausible is aggregated and anonymized.

            No other third-party analytics or tracking tools are used on this website.

            These aggregated, non-identifiable usage statistics are processed on the basis
            of our legitimate interest (Art. 6 (1)(f) GDPR) to analyze and improve our website.
            You have the right to object to this processing at any time.
            To exercise your right, please contact us at info@zauberzeug.com.

            For more details on Plausible Analytics and its data policy,
            visit <https://plausible.io/data-policy>.
        ''')


def _heading(text: str) -> ui.label:
    return ui.label(text).classes(f'{d.TEXT_SECTION_TITLE} font-medium tracking-tight mt-16')


def _subheading(text: str) -> ui.label:
    return ui.label(text).classes(f'{d.TEXT_19PX} font-medium mt-8')


def _text(content: str) -> ui.markdown:
    return ui.markdown(content).classes(f'{d.TEXT_SECONDARY} mt-4')
