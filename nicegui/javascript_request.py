from __future__ import annotations

import asyncio
from typing import Any, ClassVar, Dict


class JavaScriptRequest:
    _instances: ClassVar[Dict[str, JavaScriptRequest]] = {}

    def __init__(self, request_id: str, *, timeout: float) -> None:
        self.request_id = request_id
        self._instances[request_id] = self
        self.timeout = timeout
        self._event = asyncio.Event()
        self._result: Any = None

    @classmethod
    def resolve(cls, request_id: str, result: Any) -> None:
        """Store the result of a JavaScript request and unblock the awaiter."""
        request = cls._instances[request_id]
        request._result = result  # pylint: disable=protected-access
        request._event.set()  # pylint: disable=protected-access

    def __await__(self) -> Any:
        try:
            yield from asyncio.wait_for(self._event.wait(), self.timeout).__await__()
        except asyncio.TimeoutError as e:
            raise TimeoutError(f'JavaScript did not respond within {self.timeout:.1f} s') from e
        else:
            return self._result
        finally:
            self._instances.pop(self.request_id)
