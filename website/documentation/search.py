from fastapi.responses import JSONResponse
from rapidfuzz import fuzz, process

from nicegui import app

from ..examples import examples
from .code_extraction import get_full_code
from .content import registry

search_index: list[dict[str, str]] = []
sitewide_index: list[dict[str, str]] = []
examples_index: list[dict[str, str]] = []

_titles: list[str] = []
_contents: list[str] = []


@app.get('/static/sitewide_index.json')
def _get_sitewide_index() -> JSONResponse:
    return JSONResponse(sitewide_index)


@app.get('/static/examples_index.json')
def _get_examples_index() -> JSONResponse:
    return JSONResponse(examples_index)


def build_search_index() -> None:
    """Build search index."""
    search_index[:] = _collect_documentation_parts(include_code=False) + _collect_examples()
    sitewide_index[:] = _collect_documentation_parts(include_code=True)
    examples_index[:] = _collect_examples()
    _titles[:] = [item['title'] for item in search_index]
    _contents[:] = [item['content'] for item in search_index]


def search(query: str, *, limit: int = 100) -> list[dict[str, str]]:
    """Search the documentation index using fuzzy matching."""
    if not query or not search_index:
        return []
    title_results = process.extract(query, _titles, scorer=fuzz.WRatio, limit=limit, score_cutoff=(40 - 100 * 0.3) / 0.7)
    content_choices = {idx: _contents[idx] for _, _, idx in title_results}
    content_results = process.extract(query, content_choices, scorer=fuzz.WRatio, limit=len(content_choices))
    content_scores = {idx: score for _, score, idx in content_results}
    scored = []
    for _, title_score, idx in title_results:
        combined = title_score * 0.7 + content_scores.get(idx, 0) * 0.3
        if combined >= 40:
            scored.append((combined, idx))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [search_index[idx] for _, idx in scored[:limit]]


def _collect_documentation_parts(*, include_code: bool = False) -> list[dict[str, str]]:
    return [
        {
            'title': f'{documentation.heading.replace("*", "")}: {part.title}',
            'content': part.description or part.search_text or '',
            'format': part.description_format,
            **({'demo': get_full_code(part.demo.function) if part.demo is not None else ''} if include_code else {}),
            'url': f'/documentation/{documentation.name}#{part.link_target}',
        }
        for documentation in registry.values()
        for part in documentation.parts
    ]


def _collect_examples() -> list[dict[str, str]]:
    return [
        {
            'title': f'Example: {example.title}',
            'content': example.description,
            'format': 'md',
            'url': example.url,
        }
        for example in examples
    ]
