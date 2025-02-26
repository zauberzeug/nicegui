from pathlib import Path
from typing import Optional

import aiofiles

from nicegui import background_tasks, core, json
from nicegui.logging import log

from .persistent_dict import PersistentDict


class FilePersistentDict(PersistentDict):

    def __init__(self, filepath: Path, encoding: Optional[str] = None, *, indent: bool = False) -> None:
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

        async def backup() -> None:
            async with aiofiles.open(self.filepath, 'w', encoding=self.encoding) as f:
                await f.write(json.dumps(self, indent=self.indent))
        if core.loop:
            background_tasks.create_lazy(backup(), name=self.filepath.stem)
        else:
            core.app.on_startup(backup())

    def clear(self) -> None:
        super().clear()
        self.filepath.unlink(missing_ok=True)
