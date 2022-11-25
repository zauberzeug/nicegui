from typing import TYPE_CHECKING, Any, Coroutine, Generator

if TYPE_CHECKING:
    from .client import Client


class AsyncUpdater:

    def __init__(self, coro: Coroutine, client: 'Client') -> None:
        self.coro = coro
        self.client = client

    def __await__(self) -> Generator[Any, None, Any]:
        coro_iter = self.coro.__await__()
        iter_send, iter_throw = coro_iter.send, coro_iter.throw
        send, message = iter_send, None
        while True:
            try:
                signal = send(message)
                self.lazy_update()
            except StopIteration as err:
                return err.value
            else:
                send = iter_send
            try:
                message = yield signal
            except BaseException as err:
                send, message = iter_throw, err

    def lazy_update(self) -> None:
        for slot in self.client.slot_stack:
            slot.lazy_update()
