import asyncio

from nicegui import Client, ui

from .content import overview, redirects, registry
from .custom_restructured_text import CustomRestructuredText
from .intro import create_intro
from .rendering import render_page
from .search import build_search_index
from .tree import build_tree
from .windows import bash_window, browser_window, python_window


async def preload_pages() -> None:
    """Execute demo functions once to register all page routes."""
    with Client.auto_index_client:
        for documentation in registry.values():
            for part in documentation.parts:
                if part.demo is not None:
                    with ui.element() as container:
                        try:
                            result = part.demo.function()
                            if asyncio.iscoroutine(result):
                                await result
                        except Exception:
                            pass
                    container.delete()


__all__ = [
    'CustomRestructuredText',
    'bash_window',
    'browser_window',
    'build_search_index',
    'build_tree',
    'create_intro',
    'overview',  # ensure documentation tree is built
    'preload_pages',
    'python_window',
    'redirects',
    'registry',
    'render_page',
]
