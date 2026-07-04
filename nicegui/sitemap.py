from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

from .logging import log

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

    The ``/sitemap.xml`` route is created at startup, and only when at least one entry
    exists — an app that opts nothing in keeps its original ``404`` rather than serving
    an empty sitemap. Define your own ``@ui.page('/sitemap.xml')`` (or ``@app.get(...)``)
    to override NiceGUI's; yours takes precedence as long as it is registered before
    startup (a route added dynamically *after* startup would be shadowed).
    """

    def __init__(self) -> None:
        self._entries: dict[str, SitemapEntry] = {}
        self._decorator_opted_in: set[str] = set()
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
            Parameterized paths (containing ``{...}``), paths not starting with ``/``, and paths
            with control characters are rejected — add one entry per concrete URL instead.
        :param lastmod: ISO-8601 date or datetime of last modification, as a string
        :param changefreq: ``always``, ``hourly``, ``daily``, ``weekly``, ``monthly``, ``yearly``, or ``never``
        :param priority: relative importance from ``0.0`` to ``1.0``
            (out-of-range values are clamped, non-numeric values are ignored with a warning)
        """
        if '{' in path:
            raise ValueError(
                f'Cannot add parameterized path {path!r} to the sitemap: there is no enumerator. '
                "Add a concrete path per URL instead (e.g. app.sitemap.add('/users/alice'))."
            )
        if not path.startswith('/'):
            raise ValueError(f'Cannot add path {path!r} to the sitemap: paths must start with "/" '
                             f"(e.g. app.sitemap.add('/{path}')).")
        if any(ord(char) < 0x20 or ord(char) == 0x7f for char in path):
            raise ValueError(f'Cannot add path {path!r} to the sitemap: it contains control characters.')
        if unknown:
            raise ValueError(
                f'Unknown sitemap field(s) for {path!r}: {sorted(unknown)}. '
                f'Supported: {list(_VALID_FIELDS)}. See https://www.sitemaps.org/protocol.html'
            )
        for name, value in (('lastmod', lastmod), ('changefreq', changefreq)):
            if value is not None and not isinstance(value, str):
                raise ValueError(f'Sitemap {name} for {path!r} must be a string, '
                                 f'got {type(value).__name__}: {value!r}.')
        self._entries[path] = SitemapEntry(path, lastmod, changefreq, self._normalize_priority(path, priority))
        self._decorator_opted_in.discard(path)  # a manual add() (re)claims the path from decorator provenance

    def remove(self, path: str) -> None:
        """Retract a previously added entry. No-op if ``path`` is not present."""
        self._entries.pop(path, None)
        self._decorator_opted_in.discard(path)

    def _add_from_decorator(self, path: str, **metadata: Any) -> None:
        """Opt ``path`` in via the ``@ui.page(sitemap=...)`` decorator and record that provenance.

        Unlike :meth:`add`, this remembers that the decorator owns the entry, so a later
        ``@ui.page(path, sitemap=False)`` may retract it (see :meth:`_remove_from_decorator`).
        """
        self.add(path, **metadata)
        self._decorator_opted_in.add(path)

    def _remove_from_decorator(self, path: str) -> None:
        """Retract ``path`` ONLY if a decorator previously opted it in.

        This protects a manual ``app.sitemap.add(path)`` from being silently wiped by a plain
        ``@ui.page(path)`` (whose default ``sitemap=False`` would otherwise remove the entry).
        """
        if path in self._decorator_opted_in:
            self.remove(path)

    def reset(self) -> None:
        """Clear all entries and the base URL. (For testing.)"""
        self._entries.clear()
        self._decorator_opted_in.clear()
        self.base_url = None

    def entries(self) -> Iterator[SitemapEntry]:
        """Yield every entry that should appear in the sitemap."""
        yield from self._entries.values()

    @staticmethod
    def _normalize_priority(path: str, value: Any) -> float | None:
        """Validate and clamp a priority value at registration time, warning instead of storing a bad value.

        Returns ``None`` (priority omitted) for unset, non-numeric, or non-finite values; otherwise clamps to ``[0.0, 1.0]``.
        Validating here in :meth:`add` means a bad value warns once at registration rather than on every ``/sitemap.xml`` request.
        """
        if value is None:
            return None
        try:
            priority = float(value)
        except (TypeError, ValueError):
            log.warning('Ignoring non-numeric sitemap priority %r for %r; expected a number in [0.0, 1.0].',
                        value, path)
            return None
        if not math.isfinite(priority):  # NaN/inf would clamp to a misleading 0.0/1.0 — omit instead
            log.warning('Ignoring non-finite sitemap priority %r for %r; expected a number in [0.0, 1.0].', value, path)
            return None
        clamped = max(0.0, min(1.0, priority))
        if clamped != priority:
            log.warning('Clamping out-of-range sitemap priority %s for %r to %s (valid range [0.0, 1.0]).',
                        priority, path, clamped)
        return clamped

    @staticmethod
    def _format_priority(value: float) -> str:
        """Render a priority as a plain decimal in ``[0.0, 1.0]``.

        ``str(0.00001)`` would emit ``'1e-05'`` — scientific notation the sitemaps.org protocol
        rejects. Fixed-point formatting (trimmed, but never below one decimal place) keeps ``1.0``
        and ``0.85`` intact while avoiding sci-notation and bounding repeating decimals.
        """
        text = f'{value:.10f}'.rstrip('0')
        return f'{text}0' if text.endswith('.') else text

    def to_xml(self, base_url: str) -> str:
        """Render the sitemap as XML rooted at ``base_url`` (e.g. ``https://example.com``)."""
        # Declare the namespace as a literal root attribute rather than ET.register_namespace(),
        # which would mutate ElementTree's process-global prefix map as a side effect.
        urlset = ET.Element('urlset', {'xmlns': _NS})
        for entry in self.entries():
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = base_url.rstrip('/') + entry.path
            if entry.lastmod is not None:
                ET.SubElement(url, 'lastmod').text = entry.lastmod
            if entry.changefreq is not None:
                ET.SubElement(url, 'changefreq').text = entry.changefreq
            if entry.priority is not None:
                ET.SubElement(url, 'priority').text = self._format_priority(entry.priority)
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset, encoding='unicode')
