"""Minimal page class for Pyodide — no FastAPI, no route registration."""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from .language import Language


class page:
    """Lightweight page stub for Pyodide environments.

    Stores page configuration but does not register HTTP routes.
    Provides the same resolve_*() interface that Client and Outbox expect.
    """

    def __init__(self,
                 path: str = '/', *,
                 title: str | None = None,
                 viewport: str | None = None,
                 favicon: str | Path | None = None,
                 dark: bool | None = None,
                 language: Language = ...,  # type: ignore
                 response_timeout: float = 3.0,
                 reconnect_timeout: float | None = None,
                 **kwargs: Any,
                 ) -> None:
        self._path = path
        self.title = title
        self.viewport = viewport
        self.favicon = favicon
        self.dark = dark
        self.language = language
        self.response_timeout = response_timeout
        self.reconnect_timeout = reconnect_timeout
        self.kwargs = kwargs

    @property
    def path(self) -> str:
        return self._path

    def resolve_title(self) -> str:
        return self.title or 'NiceGUI'

    def resolve_viewport(self) -> str:
        return self.viewport or 'width=device-width, initial-scale=1'

    def resolve_dark(self) -> bool | None:
        return self.dark

    def resolve_language(self) -> Language:
        return self.language if self.language is not ... else 'en-US'  # type: ignore

    def resolve_reconnect_timeout(self) -> float:
        return self.reconnect_timeout if self.reconnect_timeout is not None else 5.0

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """No-op decorator in Pyodide — no routes to register."""
        return func
