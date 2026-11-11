import xml.etree.ElementTree as ET

from . import documentation, i18n

SITE_URL = 'https://nicegui.io'

STATIC_PATHS = ('/', '/examples', '/documentation', '/imprint_privacy')


def paths() -> list[str]:
    """Return the unprefixed paths of all indexable pages."""
    return [*STATIC_PATHS, *(f'/documentation/{name}' for name in documentation.registry if name)]


def build() -> str:
    """Build the sitemap XML listing every page in every language with its ``hreflang`` alternates."""
    urlset = ET.Element('urlset', {
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'xmlns:xhtml': 'http://www.w3.org/1999/xhtml',
    })
    for path in paths():
        alternates = i18n.alternates(path)
        for slug in i18n.LANGUAGES:
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = SITE_URL + i18n.url(path, language=slug)
            for code, alternate in alternates:
                ET.SubElement(url, 'xhtml:link', rel='alternate', hreflang=code, href=SITE_URL + alternate)
    return ET.tostring(urlset, encoding='unicode', xml_declaration=True) + '\n'
