import asyncio
import hashlib
import struct
import time
from pathlib import Path


def is_file(path: str | Path | None) -> bool:
    """Check if the path is a file that exists."""
    if not path:
        return False
    if isinstance(path, str) and path.strip().startswith('data:'):
        return False  # avoid passing data URLs to Path
    try:
        return Path(path).is_file()
    except OSError:
        return False


def hash_file_path(path: Path, *, max_time: float | None = None) -> str:
    """Hash the given path based on its string representation and optionally the last modification time of given files."""
    hasher = hashlib.sha256(path.as_posix().encode())
    if max_time is not None:
        hasher.update(struct.pack('!d', max_time))
    return hasher.hexdigest()[:32]


def unlink_with_retry(filepath: Path, *, missing_ok: bool = False, timeout: float = 1.0) -> None:
    """Unlink a file, waiting out transient ``PermissionError`` on Windows.

    A concurrent writer (e.g. a lazily scheduled storage backup) may still hold the file open;
    Windows cannot delete open files, so retry briefly until the handle is released.

    Note: The blocking wait can only help if the holder releases the file independently of the current thread.
    A writer that needs this thread's event loop to close its file (e.g. an ``aiofiles`` coroutine suspended
    on the very loop that is calling this function) cannot proceed while we sleep and exhausts the timeout.
    """
    deadline = time.monotonic() + timeout
    while not _try_unlink(filepath, missing_ok=missing_ok, deadline=deadline):
        time.sleep(0.02)


async def unlink_with_retry_async(filepath: Path, *, missing_ok: bool = False, timeout: float = 1.0) -> None:
    """Async variant of :func:`unlink_with_retry` which does not block the event loop while waiting."""
    deadline = time.monotonic() + timeout
    while not _try_unlink(filepath, missing_ok=missing_ok, deadline=deadline):
        await asyncio.sleep(0.02)


def _try_unlink(filepath: Path, *, missing_ok: bool, deadline: float) -> bool:
    """Attempt a single unlink, returning whether it succeeded or should be retried (raising otherwise)."""
    try:
        filepath.unlink(missing_ok=missing_ok)
        return True
    except PermissionError as e:
        if getattr(e, 'winerror', None) is None or time.monotonic() > deadline:
            raise  # only Windows PermissionErrors can be transient (winerror does not exist on POSIX)
        return False
