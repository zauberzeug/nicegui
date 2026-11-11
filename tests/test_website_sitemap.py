import xml.etree.ElementTree as ET

from website import documentation, sitemap

NAMESPACES = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'xhtml': 'http://www.w3.org/1999/xhtml'}


def test_sitemap_lists_every_page_in_every_language():
    """Every documentation page is listed in English and in Chinese."""
    urlset = ET.fromstring(sitemap.build())
    locations = {url.findtext('sm:loc', namespaces=NAMESPACES) for url in urlset.findall('sm:url', NAMESPACES)}
    assert 'https://nicegui.io/' in locations
    assert 'https://nicegui.io/zh' in locations
    for name in documentation.registry:
        assert f'https://nicegui.io/documentation/{name}'.rstrip('/') in locations
        assert f'https://nicegui.io/zh/documentation/{name}'.rstrip('/') in locations


def test_every_url_declares_its_language_alternates():
    """Every URL carries the hreflang links of all languages plus x-default."""
    urlset = ET.fromstring(sitemap.build())
    for url in urlset.findall('sm:url', NAMESPACES):
        links = {link.get('hreflang'): link.get('href') for link in url.findall('xhtml:link', NAMESPACES)}
        assert links.keys() == {'en-US', 'zh-CN', 'x-default'}, f'{url.findtext("sm:loc", namespaces=NAMESPACES)}'
        assert links['x-default'] == links['en-US']
        assert str(links['zh-CN']).startswith('https://nicegui.io/zh')
