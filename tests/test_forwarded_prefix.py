import pytest

from nicegui import ui
from nicegui.testing import User


async def test_forwarded_prefix_injection_is_neutralized(user: User):
    @ui.page('/')
    def page():
        ui.label('Hello')

    response = await user.http_client.get('/', headers={'X-Forwarded-Prefix': '/"></script><script>XSS</script>'})
    assert '<script>XSS' not in response.text, 'the injected tag must not survive in executable form'
    assert '%3Cscript%3EXSS' in response.text, 'dangerous characters should be percent-encoded'


@pytest.mark.parametrize('sent, expected', [
    # well-formed path prefixes pass through byte-for-byte (incl. RFC 3986 sub-delims except "&")
    (b'/api/v1', '/api/v1'),
    (b'/team-name_2.MyApp', '/team-name_2.MyApp'),
    (b"/a+b,c=d;e(f)!$'*", "/a+b,c=d;e(f)!$'*"),
    # non-ASCII can't round-trip cleanly (headers are latin-1, so the proxy's byte encoding decides the result)
    # but is always percent-encoded, never reflected raw
    ('/café'.encode(), '/caf%C3%83%C2%A9'),  # codespell:ignore
    ('/café'.encode('latin-1'), '/caf%C3%A9'),  # codespell:ignore
    # anything but a relative path is dropped, so resources can't be loaded from another origin
    (b'https://attacker.example.com', ''),
    (b'//attacker.example.com', ''),
    (b'attacker.example.com', ''),
    # "&" is encoded, so HTML character references can't turn into a protocol-relative URL inside an attribute
    (b'/a&b', '/a%26b'),
    (b'/&sol;attacker.example.com', '/%26sol;attacker.example.com'),
])
async def test_forwarded_prefix_is_reflected_in_safe_form(user: User, sent: bytes, expected: str):
    @ui.page('/')
    def page():
        ui.label('Hello')

    response = await user.http_client.get('/', headers={b'X-Forwarded-Prefix': sent})
    assert f'"{expected}/_nicegui/' in response.text
    if (raw := sent.decode('latin-1')) != expected:
        assert raw not in response.text, 'a non-passthrough prefix must never appear raw in any sink'
