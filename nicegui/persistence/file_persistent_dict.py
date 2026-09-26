import asyncio
import contextlib
from pathlib import Path

from .. import background_tasks, core, json
from ..helpers import unlink_with_retry, unlink_with_retry_async
from ..logging import log
from .persistent_dict import PersistentDict
from .serialization import dumps


class FilePersistentDict(PersistentDict):

    def __init__(self, filepath: Path, encoding: str | None = None, *, indent: bool = False) -> None:
        self.filepath = filepath
        self.encoding = encoding
        self.indent = indent
        super().__init__(data={}, on_change=self.backup)

    async def initialize(self) -> None:
        try:
            if self.filepath.exists():
                # read in a worker thread: see the cancellation note in async_backup below
                data = json.loads(await asyncio.to_thread(self.filepath.read_text, encoding=self.encoding))
            else:
                data = {}
            self.update(data)
        except Exception:
            log.warning(f'Could not load storage file {self.filepath}')

    def initialize_sync(self) -> None:
        try:
            if self.filepath.exists():
                data = json.loads(self.filepath.read_text(encoding=self.encoding))
            else:
                data = {}
            self.update(data)
        except Exception:
            log.warning(f'Could not load storage file {self.filepath}')

    def backup(self) -> None:
        """Back up the data to the given file path."""
        if not self.filepath.exists():
            if not self:
                return
            self.filepath.parent.mkdir(exist_ok=True)

        tmp_filepath = self.filepath.with_name(self.filepath.name + '.tmp')

        @background_tasks.await_on_shutdown
        async def async_backup() -> None:
            if not self:
                tmp_filepath.unlink(missing_ok=True)
                await unlink_with_retry_async(self.filepath, missing_ok=True)
                return
            # open, write and close in a single worker-thread call: any cancellation point between
            # opening and closing the file could strand an open handle, surfacing as a ResourceWarning
            # (not run.io_bound, which would skip the write while the app is stopping)
            await asyncio.to_thread(tmp_filepath.write_text,
                                    dumps(self, str(self.filepath), indent=self.indent), encoding=self.encoding)
            with contextlib.suppress(FileNotFoundError):  # a concurrent Storage.clear() may have swept the temp file
                tmp_filepath.replace(self.filepath)

        if core.is_loop_running():
            background_tasks.create_lazy(async_backup(), name=self.filepath.stem)
        elif not self:
            tmp_filepath.unlink(missing_ok=True)
            unlink_with_retry(self.filepath, missing_ok=True)
        else:
            tmp_filepath.write_text(dumps(self, str(self.filepath), indent=self.indent), encoding=self.encoding)
            tmp_filepath.replace(self.filepath)
