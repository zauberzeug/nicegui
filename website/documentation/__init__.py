from .content import overview, redirects, registry
from .intro import create_intro
from .rendering import render_page
from .search import build_search_index
from .windows import bash_window, browser_window, python_window

__all__ = [
    'bash_window',
    'browser_window',
    'build_search_index',
    'create_intro',
    'overview',  # ensure documentation tree is built
    'python_window',
    'registry',
    'redirects',
    'render_page',
]
