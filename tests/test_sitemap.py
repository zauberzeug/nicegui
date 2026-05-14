import xml.etree.ElementTree as ET

import pytest
from fastapi.testclient import TestClient

from nicegui import app, core, ui
from nicegui.sitemap import Sitemap

NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'


# -------------------------------------------------------------------- Sitemap class (pure unit)


def test_sitemap_is_empty_by_default():
    assert list(Sitemap().entries()) == []


def test_add_then_remove_round_trips():
    s = Sitemap()
    s.add('/a')
    s.add('/b', changefreq='daily', priority=0.5)
    assert {e.path for e in s.entries()} == {'/a', '/b'}
    s.remove('/a')
    assert {e.path for e in s.entries()} == {'/b'}
    s.remove('/missing')  # no-op


def test_add_replaces_metadata_for_same_path():
    s = Sitemap()
    s.add('/a', priority=0.1)
    s.add('/a', priority=0.9)
    entry = next(s.entries())
    assert entry.priority == 0.9


def test_add_rejects_parameterized_paths():
    s = Sitemap()
    with pytest.raises(ValueError, match=r"Cannot add parameterized path '/user/\{user_id\}'"):
        s.add('/user/{user_id}')


def test_to_xml_uses_sitemap_namespace_and_metadata():
    s = Sitemap()
    s.add('/a', lastmod='2026-05-14', changefreq='weekly', priority=0.8)
    root = ET.fromstring(s.to_xml('https://example.com'))
    assert root.tag == f'{NS}urlset'
    url = root.find(f'{NS}url')
    assert url is not None
    assert url.findtext(f'{NS}loc') == 'https://example.com/a'
    assert url.findtext(f'{NS}lastmod') == '2026-05-14'
    assert url.findtext(f'{NS}changefreq') == 'weekly'
    assert url.findtext(f'{NS}priority') == '0.8'


def test_to_xml_escapes_special_characters():
    s = Sitemap()
    s.add('/search?q=<x>&y=1')
    root = ET.fromstring(s.to_xml('https://example.com'))
    assert root.findtext(f'{NS}url/{NS}loc') == 'https://example.com/search?q=<x>&y=1'


# ----------------------------------------------------- @ui.page decorator integration


def test_default_does_not_register(nicegui_reset_globals):
    @ui.page('/secret')
    def _secret():
        ui.label('secret')

    assert list(app.sitemap.entries()) == []


def test_sitemap_true_registers(nicegui_reset_globals):
    @ui.page('/about', sitemap=True)
    def _about():
        ui.label('about')

    assert {e.path for e in app.sitemap.entries()} == {'/about'}


def test_sitemap_dict_registers_with_metadata(nicegui_reset_globals):
    @ui.page('/', sitemap={'changefreq': 'daily', 'priority': 1.0})
    def _home():
        ui.label('home')

    entry = next(app.sitemap.entries())
    assert entry.path == '/'
    assert entry.changefreq == 'daily'
    assert entry.priority == 1.0


def test_sitemap_false_after_true_retracts(nicegui_reset_globals):
    @ui.page('/about', sitemap=True)
    def _included():
        ui.label('about')

    @ui.page('/about', sitemap=False)
    def _excluded():
        ui.label('about')

    assert list(app.sitemap.entries()) == []


@pytest.mark.parametrize('opt_in', [True, {'changefreq': 'daily'}])
def test_opting_a_parameterized_page_in_raises(opt_in, nicegui_reset_globals):
    with pytest.raises(ValueError, match='Cannot add parameterized path'):
        @ui.page('/user/{user_id}', sitemap=opt_in)
        def _user(user_id: str):
            ui.label(user_id)


def test_unknown_sitemap_field_raises_on_decorator(nicegui_reset_globals):
    with pytest.raises(ValueError, match=r"Unknown sitemap field\(s\) for '/about': \['typo'\]"):
        @ui.page('/about', sitemap={'typo': 'oops'})
        def _about():
            ui.label('about')


def test_unknown_sitemap_field_raises_on_direct_add():
    s = Sitemap()
    with pytest.raises(ValueError, match=r"Unknown sitemap field\(s\) for '/a': \['lastmode'\]"):
        s.add('/a', lastmode='2026-05-14')  # typo of lastmod


# ------------------------------------------------- /sitemap.xml endpoint (FastAPI TestClient)


def _locations(text: str) -> set[str]:
    root = ET.fromstring(text)
    return {loc.text for loc in root.iter(f'{NS}loc') if loc.text is not None}


def test_endpoint_serves_xml_with_absolute_urls(nicegui_reset_globals):
    @ui.page('/', sitemap=True)
    def _home():
        ui.label('home')

    response = TestClient(core.app).get('/sitemap.xml')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('application/xml')
    locations = _locations(response.text)
    assert locations
    for loc in locations:
        assert loc.startswith(('http://', 'https://'))


def test_endpoint_honors_base_url_override(nicegui_reset_globals):
    @ui.page('/', sitemap=True)
    def _home():
        ui.label('home')

    app.sitemap.base_url = 'https://nicegui.io'
    response = TestClient(core.app).get('/sitemap.xml')
    assert all(loc.startswith('https://nicegui.io/') for loc in _locations(response.text))


def test_endpoint_honors_forwarded_prefix(nicegui_reset_globals):
    @ui.page('/', sitemap=True)
    def _home():
        ui.label('home')

    response = TestClient(core.app).get('/sitemap.xml', headers={'X-Forwarded-Prefix': '/app'})
    assert any('/app/' in loc for loc in _locations(response.text))


def test_endpoint_reflects_documentation_pattern(nicegui_reset_globals):
    """Mirror nicegui.io: stacked decorators (one parameterized) + manual adds for concrete docs URLs."""
    @ui.page('/', sitemap=True)
    @ui.page('/examples', sitemap=True)
    @ui.page('/documentation', sitemap=True)
    @ui.page('/documentation/{path:path}')  # parameterized → skipped
    def _main():
        ui.label('main')

    for name in ['button', 'label']:
        app.sitemap.add(f'/documentation/{name}', changefreq='weekly')

    locations = _locations(TestClient(core.app).get('/sitemap.xml').text)
    assert any(loc.endswith('/examples') for loc in locations)
    assert any(loc.endswith('/documentation') for loc in locations)
    assert any(loc.endswith('/documentation/button') for loc in locations)
    assert any(loc.endswith('/documentation/label') for loc in locations)
    assert not any('{' in loc for loc in locations)
