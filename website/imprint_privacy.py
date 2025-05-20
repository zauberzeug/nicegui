from nicegui import ui
from website.documentation.rendering import section_heading, subheading
from website.header import add_head_html, add_header


def create():
    add_head_html()
    add_header()
    ui.page_title('Imprint & Privacy | NiceGUI')

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):
        section_heading('', 'Imprint')
        subheading('Zauberzeug GmbH')
        ui.markdown('''
            Hohenholter Str. 43, 48329 Havixbeck, Germany

            Represented by Rodion (Rodja) Trappe

            Phone: +49 2507 3817, Email: info@zauberzeug.com
        ''')

        subheading('Registry entry')
        ui.markdown('''
            Registry court: Amtsgericht Coesfeld, Registry number: HRB 14215
        ''')

        subheading('Tax')
        ui.markdown('''
            Sales tax identification number according to §27a Sales Tax Act: DE286384205
        ''')

        section_heading('', 'Privacy Policy')
        ui.markdown('''
            We use [Plausible Analytics](https://plausible.io) to understand how you interact with our site.
            Plausible Analytics is a privacy-first analytics tool that does not use
            cookies or collect any personal data or personally identifiable information (PII).
            All data collected by Plausible is aggregated and anonymized.

            No other third-party analytics or tracking tools are used on this website.

            These aggregated, non-identifiable usage statistics are processed on the basis
            of our legitimate interest (Art. 6 (1)(f) GDPR) to analyze and improve our website.
            You have the right to object to this processing at any time. To exercise your right,
            please contact us at info@zauberzeug.com.

            For more details on Plausible Analytics and its data policy,
            visit <https://plausible.io/data-policy>
        ''')
