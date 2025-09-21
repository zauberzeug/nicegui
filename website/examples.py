from dataclasses import dataclass, field
from pathlib import Path
from typing import List

PATH = Path(__file__).parent.parent / 'examples'


@dataclass
class Example:
    title: str
    description: str
    url: str = field(init=False)
    screenshot: str = field(init=False, default='screenshot.webp')

    def __post_init__(self) -> None:
        """Post-initialization hook."""
        name = self.title.lower().replace(' ', '_').replace('-', '_')
        content = [p for p in (PATH / name).glob('*') if not p.name.startswith(('__pycache__', '.', 'test_'))]
        filename = 'main.py' if len(content) == 1 else ''
        self.url = f'https://github.com/zauberzeug/nicegui/tree/main/examples/{name}/{filename}'
        # prefer a per-example screenshot if it exists, otherwise use the placeholder
        screenshot_path = PATH / name / 'screenshot.webp'
        placeholder = PATH / 'placeholder.webp'
        self.screenshot = str(screenshot_path) if screenshot_path.exists() else str(placeholder)


readme_files_paths: List[Path]  = sorted([ (PATH / f.name / 'README.md') for f in PATH.iterdir() if f.is_dir(follow_symlinks=False)])
examples: List[Example] = []
for path in readme_files_paths:
    title = description = path.parent.name.replace('_', ' ').title()
    if path.exists():
        lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if lines:
            # Use first non-empty line as title, second one as description if available
            title = lines[0].lstrip('#').strip()
            description = lines[1] if len(lines) > 1 else description
    examples.append(Example(title=title, description=description))
