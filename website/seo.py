"""SEO utilities for the NiceGUI documentation website."""
import html
import json
import re

SITE_URL = 'https://nicegui.io'
SITE_NAME = 'NiceGUI'
TAGLINE = 'Python-Based UI Framework'
DEFAULT_DESCRIPTION = (
    'NiceGUI is an easy-to-use, Python-based UI framework, '
    'which shows up in your web browser. '
    'Create buttons, dialogs, Markdown, 3D scenes, plots and much more.'
)
OG_IMAGE_URL = f'{SITE_URL}/logo_square.png'
OG_IMAGE_WIDTH = 290
OG_IMAGE_HEIGHT = 290
MIN_DESCRIPTION_LENGTH = 50


def meta(name: str, content: str) -> str:
    return f'<meta name="{name}" content="{html.escape(content, quote=True)}" />'


def meta_property(prop: str, content: str) -> str:
    return f'<meta property="{prop}" content="{html.escape(content, quote=True)}" />'


def canonical_link(path: str) -> str:
    url = SITE_URL + path
    return f'<link rel="canonical" href="{html.escape(url, quote=True)}" />'


def open_graph_tags(*, title: str, description: str, url: str, og_type: str = 'website') -> str:
    return '\n'.join([
        meta_property('og:title', title),
        meta_property('og:description', description),
        meta_property('og:url', url),
        meta_property('og:type', og_type),
        meta_property('og:site_name', SITE_NAME),
        meta_property('og:locale', 'en_US'),
        meta_property('og:image', OG_IMAGE_URL),
        meta_property('og:image:alt', f'{SITE_NAME} logo'),
        meta_property('og:image:width', str(OG_IMAGE_WIDTH)),
        meta_property('og:image:height', str(OG_IMAGE_HEIGHT)),
    ])


def twitter_card_tags(*, title: str, description: str) -> str:
    return '\n'.join([
        meta('twitter:card', 'summary'),
        meta('twitter:title', title),
        meta('twitter:description', description),
        meta('twitter:image', OG_IMAGE_URL),
    ])


def noscript_fallback(*, title: str, description: str) -> str:
    esc = html.escape
    return (
        f'<noscript>'
        f'<h1>{esc(title)}</h1>'
        f'<p>{esc(description)}</p>'
        f'<p>Visit <a href="{SITE_URL}">{SITE_URL}</a> for the full NiceGUI documentation.</p>'
        f'</noscript>'
    )


def page_seo_html(*, title: str, description: str, path: str, og_type: str = 'website') -> str:
    url = SITE_URL + path
    parts = [
        meta('description', description),
        canonical_link(path),
        open_graph_tags(title=title, description=description, url=url, og_type=og_type),
        twitter_card_tags(title=title, description=description),
    ]
    return '\n'.join(parts)


def breadcrumb_jsonld(items: list[tuple[str, str]]) -> str:
    """Generate BreadcrumbList JSON-LD structured data.

    :param items: list of (name, path) tuples for each breadcrumb level
    """
    ld = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {
                '@type': 'ListItem',
                'position': i + 1,
                'name': name,
                'item': SITE_URL + path,
            }
            for i, (name, path) in enumerate(items)
        ],
    }
    payload = json.dumps(ld, separators=(',', ':')).replace('</', '<\\/')
    return f'<script type="application/ld+json">{payload}</script>'


def extract_description(text: str, max_length: int = 160) -> str | None:
    """Extract a clean description from markdown/rst text, or None if too short."""
    text = re.split(r'\n\s*:param\s', text, maxsplit=1)[0]
    text = re.split(r'\n\s*:type\s', text, maxsplit=1)[0]
    text = re.split(r'\n\s*:returns?\s', text, maxsplit=1)[0]
    text = re.sub(r'`([^`<]+)\s*<[^>]+>`_', r'\1', text)  # rst link: `text <url>`_ -> text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # md link: [text](url) -> text
    text = re.sub(r'`([^`]*)`', r'\1', text)  # `code` -> code
    text = re.sub(r'`', '', text)
    text = re.sub(r'\*+([^*]+)\*+', r'\1', text)  # *bold*/**bold** -> bold
    text = re.sub(r'(?<!\w)_([^_]+)_(?!\w)', r'\1', text)  # _italic_ -> italic
    text = re.sub(r'<[^>]+>', '', text)  # remove HTML tags
    text = re.sub(r'\s+', ' ', text).strip()
    if not text or len(text) < MIN_DESCRIPTION_LENGTH:
        return None
    if len(text) > max_length:
        text = text[:max_length - 3].rsplit(' ', 1)[0] + '...'
    return text
