from dataclasses import dataclass, field
from pathlib import Path
from typing import List


PATH = Path(__file__).parent.parent / 'examples'


@dataclass
class Example:
    title: str
    description: str
    url: str = field(init=False)
    screenshot: str = field(init=False)

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


# Discover all examples folders (no symlink recursion)
examples_folders: List[Path] = sorted(
    (p for p in PATH.iterdir() if p.is_dir(follow_symlinks=False)),
    key=lambda r: r.name.lower(),
)

examples: List[Example] = []
for folder in examples_folders:
    title = description = folder.name.replace('_', ' ').title()
    readme_file = folder / 'README.md'

    if readme_file.exists():
        try:
            text = readme_file.read_text(encoding='utf-8')
            non_empty_lines = [line.strip() for line in text.splitlines() if line.strip()]
            # first non-empty line is the title (strip any leading markdown header markers)
            title = non_empty_lines[0].lstrip('#').strip() if non_empty_lines else title
            # second non-empty line (if present) is used as description
            description = non_empty_lines[1].strip() if len(non_empty_lines) > 1 else description
        except Exception as exc:
            # Log the error with traceback so it can be diagnosed, but continue with defaults
            print(f"Failed to read/parse README '{readme_file}' for example '{folder.name}'", exc)

    examples.append(Example(title=title, description=description))
