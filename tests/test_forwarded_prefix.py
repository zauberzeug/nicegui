import pytest

from nicegui import ui
from nicegui.testing import User


async def test_forwarded_prefix_injection_is_neutralized(user: User):
    @ui.page('/')
    def page():
        ui.label('Hello')

    payload = '"></script><script>PWNED</script>'
    response = await user.http_client.get('/', headers={'X-Forwarded-Prefix': payload})
    assert payload not in response.text, 'X-Forwarded-Prefix must not be reflected raw into the page'
    assert '<script>PWNED' not in response.text, 'the injected tag must not survive in executable form'
    assert '%3Cscript%3EPWNED' in response.text, 'dangerous characters should be percent-encoded'


@pytest.mark.parametrize('prefix', [
    '/app',
    '/api/v1',
    '/team-name_2',
    '/MyApp.v2',
    '/a+b,c=d&e(f)',  # RFC 3986 path-legal sub-delims must pass through unchanged
])
async def test_forwarded_prefix_valid_path_is_unchanged(user: User, prefix: str):
    @ui.page('/')
    def page():
        ui.label('Hello')

    response = await user.http_client.get('/', headers={'X-Forwarded-Prefix': prefix})
    assert f'{prefix}/_nicegui/' in response.text, 'a legitimate URL-path prefix must pass through byte-for-byte'


@pytest.mark.parametrize('raw_bytes, expected', [
    ('/café'.encode(), '/caf%C3%83%C2%A9'),  # UTF-8 proxy: latin-1-decoded first -> mojibake. codespell:ignore
    ('/café'.encode('latin-1'), '/caf%C3%A9'),  # latin-1 proxy: decodes cleanly. codespell:ignore
])
async def test_forwarded_prefix_non_ascii_is_encoded_never_raw(user: User, raw_bytes: bytes, expected: str):
    """A non-ASCII prefix never round-trips cleanly (HTTP headers are latin-1 by spec, so the byte encoding the
    proxy uses decides the result) — but it is always percent-encoded and never reflected as raw, executable text.
    """
    @ui.page('/')
    def page():
        ui.label('Hello')

    response = await user.http_client.get('/', headers={'X-Forwarded-Prefix': raw_bytes})
    assert f'{expected}/_nicegui/' in response.text
    assert '/café/_nicegui' not in response.text, 'must never be reflected as raw non-ASCII'
