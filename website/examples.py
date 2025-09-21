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


# discover README files for each example directory (no symlink recursion)
readme_files_paths: List[Path] = sorted(
    (p / 'README.md' for p in PATH.iterdir() if p.is_dir(follow_symlinks=False)),
    key=lambda p: p.parent.name.lower(),
)

examples: List[Example] = []
for readme in readme_files_paths:
    # sensible defaults derived from the folder name
    default_title = readme.parent.name.replace('_', ' ').title()
    default_description = default_title

    title = default_title
    description = default_description

    if readme.exists():
        try:
            text = readme.read_text(encoding='utf-8')
            nonempty = [line.strip() for line in text.splitlines() if line.strip()]
            if nonempty:
                # first non-empty line is the title (strip any leading markdown header markers)
                title_candidate = nonempty[0].lstrip('#').strip()
                title = title_candidate or default_title
                # second non-empty line (if present) is used as description
                description = nonempty[1] if len(nonempty) > 1 else default_description
        except Exception:
            # keep defaults on read/encoding errors
            pass

    examples.append(Example(title=title, description=description))
