import json
from pathlib import Path

WEBSITE_PATH = Path(__file__).parent.parent / 'website'


def test_special_sponsor_logos_exist():
    """The logo file names are derived from the sponsor keys in github_stats.json.

    Match against the directory listing instead of using Path.exists(),
    which is case-insensitive on macOS and would miss a mismatch that breaks the logo on the Linux server.
    """
    names = {path.name for path in (WEBSITE_PATH / 'static' / 'sponsors').iterdir()}
    stats = json.loads((WEBSITE_PATH / 'github_stats.json').read_text(encoding='utf-8'))
    for sponsor in stats['special']:
        assert f'{sponsor}.webp' in names or {f'{sponsor}.light.webp', f'{sponsor}.dark.webp'} <= names, \
            f'no logo for sponsor "{sponsor}" in website/static/sponsors'
