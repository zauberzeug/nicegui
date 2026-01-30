from pathlib import Path

import aiofiles

from .. import background_tasks, core, json
from ..logging import log
from .persistent_dict import PersistentDict


class FilePersistentDict(PersistentDict):

    def __init__(self, filepath: Path, encoding: str | None = None, *, indent: bool = False) -> None:
        self.filepath = filepath
        self.encoding = encoding
        self.indent = indent
        super().__init__(data={}, on_change=self.backup)

    async def initialize(self) -> None:
        try:
            if self.filepath.exists():
                async with aiofiles.open(self.filepath, encoding=self.encoding) as f:
                    data = json.loads(await f.read())
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

        @background_tasks.await_on_shutdown
        async def async_backup() -> None:
            async with aiofiles.open(self.filepath, 'w', encoding=self.encoding) as f:
                await f.write(json.dumps(self, indent=self.indent))

        if core.loop and core.loop.is_running():
            background_tasks.create_lazy(async_backup(), name=self.filepath.stem)
        else:
            self.filepath.write_text(json.dumps(self, indent=self.indent), encoding=self.encoding)

    def clear(self) -> None:
        super().clear()
        self.filepath.unlink(missing_ok=True)
