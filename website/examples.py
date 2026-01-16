from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from nicegui import app

PATH = Path(__file__).parent.parent / 'examples'


@dataclass
class Example:
    title: str
    description: str
    url: str
    screenshot: str

    @classmethod
    def from_path(cls, path: Path) -> Example:
        """Create an Example from a directory containing a README.md file and a screenshot.webp file."""
        lines = (path / 'README.md').read_text(encoding='utf-8').splitlines()
        return cls(
            title=lines[0].removeprefix('# '),
            description=lines[2].removesuffix('.'),
            url=f'https://github.com/zauberzeug/nicegui/tree/main/examples/{path.name}/main.py',
            screenshot=app.add_media_file(
                local_file=path / 'screenshot.webp',
                url_path=f'/examples/images/{path.name}/screenshot.webp',
            ),
        )


examples = [Example.from_path(p) for p in sorted(PATH.iterdir()) if p.is_dir()]
