from __future__ import annotations

import xml.etree.ElementTree as ET
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'


@dataclass
class SitemapEntry:
    path: str
    lastmod: str | None = None
    changefreq: str | None = None
    priority: float | None = None


_VALID_FIELDS = ('lastmod', 'changefreq', 'priority')


class Sitemap:
    """Registry of URLs served at ``/sitemap.xml``.

    Pages are **opt-in**: NiceGUI does not enumerate ``@ui.page`` routes anywhere
    public by default, so an app may rely on unguessable URLs (e.g.
    ``/super-secret-page-only-i-know``) as a soft auth signal. Auto-publishing
    those into a sitemap would silently break that pattern.

    Opt in per-page with ``@ui.page('/path', sitemap=True)`` or
    ``@ui.page('/path', sitemap={'changefreq': 'daily', 'priority': 0.9})``.
    For URLs that don't map one-to-one to an ``@ui.page`` decoration —
    ``ui.sub_pages`` routes (per-request, not knowable at startup), parameterized
    ``@ui.page('/foo/{name}')`` routes (no enumerator), or hand-curated entries —
    iterate over your own index and call ``app.sitemap.add('/path', ...)``::

        @ui.page('/documentation/{path:path}')
        def docs_page(): ...

        for name in documentation_registry:
            app.sitemap.add(f'/documentation/{name}', changefreq='weekly')

    Set ``app.sitemap.base_url = 'https://example.com'`` to pin the canonical
    URL. If unset, the URL is derived from the incoming request (correct in dev
    and behind any reverse proxy configured to populate uvicorn's proxy headers).
    """

    def __init__(self) -> None:
        self._entries: dict[str, SitemapEntry] = {}
        self.base_url: str | None = None

    def add(self,
            path: str,
            *,
            lastmod: str | None = None,
            changefreq: str | None = None,
            priority: float | None = None,
            **unknown: Any,
            ) -> None:
        """Include ``path`` in the sitemap, replacing any prior entry for the same path.

        :param path: concrete route path starting with ``/`` (e.g. ``/docs/intro``).
            Parameterized paths (containing ``{...}``) are rejected — add one entry per concrete URL instead.
        :param lastmod: ISO-8601 date or datetime of last modification
        :param changefreq: ``always``, ``hourly``, ``daily``, ``weekly``, ``monthly``, ``yearly``, or ``never``
        :param priority: relative importance from ``0.0`` to ``1.0``
        """
        if '{' in path:
            raise ValueError(
                f'Cannot add parameterized path {path!r} to the sitemap: there is no enumerator. '
                "Add a concrete path per URL instead (e.g. app.sitemap.add('/users/alice'))."
            )
        if unknown:
            raise ValueError(
                f'Unknown sitemap field(s) for {path!r}: {sorted(unknown)}. '
                f'Supported: {list(_VALID_FIELDS)}. See https://www.sitemaps.org/protocol.html'
            )
        self._entries[path] = SitemapEntry(path, lastmod, changefreq, priority)

    def remove(self, path: str) -> None:
        """Retract a previously added entry. No-op if ``path`` is not present."""
        self._entries.pop(path, None)

    def reset(self) -> None:
        """Clear all entries and the base URL. (For testing.)"""
        self._entries.clear()
        self.base_url = None

    def entries(self) -> Iterator[SitemapEntry]:
        """Yield every entry that should appear in the sitemap."""
        yield from self._entries.values()

    def to_xml(self, base_url: str) -> str:
        """Render the sitemap as XML rooted at ``base_url`` (e.g. ``https://example.com``)."""
        ET.register_namespace('', _NS)
        urlset = ET.Element(f'{{{_NS}}}urlset')
        for entry in self.entries():
            url = ET.SubElement(urlset, f'{{{_NS}}}url')
            ET.SubElement(url, f'{{{_NS}}}loc').text = base_url.rstrip('/') + entry.path
            if entry.lastmod is not None:
                ET.SubElement(url, f'{{{_NS}}}lastmod').text = entry.lastmod
            if entry.changefreq is not None:
                ET.SubElement(url, f'{{{_NS}}}changefreq').text = entry.changefreq
            if entry.priority is not None:
                ET.SubElement(url, f'{{{_NS}}}priority').text = f'{entry.priority:.1f}'
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset, encoding='unicode')
