import os
import sys
from pathlib import Path

if sys.platform == 'win32':
    import msvcrt  # pylint: disable=import-error
else:
    import fcntl


class FileLock:
    """Exclusive, non-blocking, advisory file lock that auto-releases on process death."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._fd: int | None = None

    def acquire(self) -> bool:
        """Acquire the lock. Return True on success, False if another process holds it."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(self.path, os.O_CREAT | os.O_RDWR)
        try:
            if sys.platform == 'win32':
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            else:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            os.close(fd)
            return False
        self._fd = fd
        return True

    def release(self) -> None:
        """Release the lock if held by this instance."""
        if self._fd is None:
            return
        if sys.platform == 'win32':
            msvcrt.locking(self._fd, msvcrt.LK_UNLCK, 1)
        else:
            fcntl.flock(self._fd, fcntl.LOCK_UN)
        os.close(self._fd)
        self._fd = None
