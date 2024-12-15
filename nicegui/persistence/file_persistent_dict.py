from pathlib import Path
from typing import Optional

import aiofiles

from nicegui import background_tasks, core, json, observables
from nicegui.logging import log


class FilePersistentDict(observables.ObservableDict):

    def __init__(self, filepath: Path, encoding: Optional[str] = None, *, indent: bool = False) -> None:
        self.filepath = filepath
        self.encoding = encoding
        self.indent = indent
        try:
            data = json.loads(filepath.read_text(encoding)) if filepath.exists() else {}
        except Exception:
            log.warning(f'Could not load storage file {filepath}')
            data = {}
        super().__init__(data, on_change=self.backup)

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
