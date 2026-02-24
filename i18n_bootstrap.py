#!/usr/bin/env python3
"""Bootstrap and update website/translations/ from t() calls, documentation registry, and examples.

Extracts translatable strings from three sources:
1. Static: AST parsing of t() calls in website/**/*.py
2. Runtime: importing the documentation registry to enumerate page titles, subtitles, and part descriptions
3. Static: titles and descriptions from examples/*/README.md files

Each language is stored in a separate CSV file linked by SHA-256 hash of the English text.

Usage:
    python i18n_bootstrap.py                    # sync CSVs with code
    python i18n_bootstrap.py --add-language ja  # add a new language CSV
"""
import argparse
import ast
import csv
import hashlib
import inspect
import re
import sys
from pathlib import Path

WEBSITE_DIR = Path(__file__).parent / 'website'
EXAMPLES_DIR = Path(__file__).parent / 'examples'
TRANSLATIONS_DIR = WEBSITE_DIR / 'translations'

TRANSLATING_FUNCTIONS = {'t', 'subheading', '_main_page_demo'}


def _sha256(text: str) -> str:
    """Compute the SHA-256 hex digest of a UTF-8 encoded string."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def extract_t_strings(directory: Path) -> set[str]:
    """Extract all string arguments from t() and other auto-translating calls in Python files."""
    strings: set[str] = set()
    for py_file in sorted(directory.rglob('*.py')):
        try:
            tree = ast.parse(py_file.read_text(encoding='utf-8'), filename=str(py_file))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in TRANSLATING_FUNCTIONS
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                strings.add(node.args[0].value)
    return strings


def extract_example_strings(examples_dir: Path) -> set[str]:
    """Extract translatable titles and descriptions from example README.md files."""
    strings: set[str] = set()
    for path in sorted(examples_dir.iterdir()):
        readme = path / 'README.md'
        if not readme.exists():
            continue
        lines = readme.read_text(encoding='utf-8').splitlines()
        if len(lines) >= 1:
            strings.add(lines[0].removeprefix('# '))
        if len(lines) >= 3:
            strings.add(lines[2].removesuffix('.'))
    return strings


_PARAM_RE = re.compile(r'\s*:param \w+:\s*(.*)')


def extract_docstring_parts(doc: str) -> set[str]:
    """Extract translatable parts from a docstring: intro text and individual :param descriptions."""
    strings: set[str] = set()
    if ':param' not in doc:
        strings.add(doc)
        return strings
    intro_lines: list[str] = []
    for line in doc.splitlines():
        m = _PARAM_RE.match(line)
        if m:
            desc = m.group(1).strip()
            if desc:
                strings.add(desc)
        else:
            intro_lines.append(line)
    intro = '\n'.join(intro_lines).strip()
    if intro:
        strings.add(intro)
    return strings


def _extract_reference_strings(class_obj: type, strings: set[str]) -> None:
    """Extract translatable strings from a class's reference documentation."""
    from nicegui import binding

    doc = class_obj.__doc__ or class_obj.__init__.__doc__
    if doc and ':param' in doc:
        from nicegui.elements.markdown import remove_indentation
        description = remove_indentation(doc.split('\n', 1)[-1])
        strings |= extract_docstring_parts(description)

    mro = [base for base in class_obj.__mro__ if base.__module__.startswith('nicegui.')]
    for base in mro:
        for name in dir(base):
            if name.startswith('_'):
                continue
            attr = base.__dict__.get(name)
            if not (inspect.isfunction(attr) or inspect.ismethod(attr) or
                    isinstance(attr, (staticmethod, classmethod, property, binding.BindableProperty))):
                continue
            obj = getattr(base, name, None)
            if obj is None:
                continue
            docstring = inspect.getdoc(obj)
            if docstring:
                strings |= extract_docstring_parts(docstring)


def extract_doc_strings() -> set[str]:
    """Import the documentation registry and extract translatable strings."""
    strings: set[str] = set()
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from website.documentation.content.doc.api import registry
        for page in registry.values():
            if page.title:
                strings.add(page.title)
                strings.add(page.title.replace('*', ''))
            if page.subtitle:
                strings.add(page.subtitle)
            for part in page.parts:
                if part.title:
                    strings.add(part.title)
                if part.description:
                    strings |= extract_docstring_parts(part.description)
                if part.reference:
                    _extract_reference_strings(part.reference, strings)
    except Exception as e:
        print(f'Warning: could not import documentation registry: {e}')
        print('Only t() strings from source code will be included.')
    return strings


def read_en_csv(path: Path) -> dict[str, str]:
    """Read en.csv and return {sha256: english_text}."""
    result: dict[str, str] = {}
    if not path.exists():
        return result
    with path.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            h = row.get('sha256', '')
            text = row.get('text', '')
            if h and text:
                result[h] = text
    return result


def read_lang_csv(path: Path) -> dict[str, str]:
    """Read a language CSV and return {sha256: translation}."""
    result: dict[str, str] = {}
    if not path.exists():
        return result
    with path.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            h = row.get('sha256', '')
            text = row.get('text', '')
            if h:
                result[h] = text
    return result


def write_csv(path: Path, rows: list[tuple[str, str]]) -> None:
    """Write a CSV with sha256,text columns, sorted by sha256."""
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['sha256', 'text'], quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for sha, text in sorted(rows, key=lambda r: r[0]):
            writer.writerow({'sha256': sha, 'text': text})


def main() -> None:
    parser = argparse.ArgumentParser(description='Bootstrap/update website translation CSVs.')
    parser.add_argument('--add-language', action='append', default=[], help='Add a new language CSV')
    parser.add_argument('--no-registry', action='store_true', help='Skip documentation registry enumeration')
    args = parser.parse_args()

    TRANSLATIONS_DIR.mkdir(exist_ok=True)

    code_strings = extract_t_strings(WEBSITE_DIR)
    example_strings = extract_example_strings(EXAMPLES_DIR)
    if not args.no_registry:
        doc_strings = extract_doc_strings()
        all_strings = code_strings | doc_strings | example_strings
        print(f'Found {len(code_strings)} t() strings + {len(doc_strings)} doc registry strings + {len(example_strings)} example strings')
    else:
        all_strings = code_strings | example_strings
        print(f'Found {len(code_strings)} t() strings + {len(example_strings)} example strings (registry skipped)')

    # Compute hashes for all current strings
    current_hashes: dict[str, str] = {}  # sha256 -> english
    for english in all_strings:
        current_hashes[_sha256(english)] = english

    # Read existing en.csv
    en_file = TRANSLATIONS_DIR / 'en.csv'
    existing_en = read_en_csv(en_file)

    # Determine added/removed
    new_hashes = set(current_hashes.keys()) - set(existing_en.keys())
    removed_hashes = set(existing_en.keys()) - set(current_hashes.keys())

    # Write en.csv
    en_rows = [(h, current_hashes[h]) for h in current_hashes]
    write_csv(en_file, en_rows)

    # Discover existing language CSVs
    existing_langs: list[str] = []
    for lang_file in sorted(TRANSLATIONS_DIR.glob('*.csv')):
        lang = lang_file.stem
        if lang != 'en':
            existing_langs.append(lang)

    # Add new languages
    for lang in args.add_language:
        if lang not in existing_langs:
            existing_langs.append(lang)

    # Update each language CSV
    for lang in existing_langs:
        lang_file = TRANSLATIONS_DIR / f'{lang}.csv'
        existing_translations = read_lang_csv(lang_file)

        # Build updated rows: keep existing translations, add empty rows for new hashes
        lang_rows: list[tuple[str, str]] = []
        for h in current_hashes:
            translation = existing_translations.get(h, '')
            lang_rows.append((h, translation))

        write_csv(lang_file, lang_rows)

    total = len(current_hashes)
    print(f'Wrote {TRANSLATIONS_DIR}: {total} strings, {len(new_hashes)} added, {len(removed_hashes)} removed, '
          f'{len(existing_langs)} language(s): {", ".join(existing_langs)}')


if __name__ == '__main__':
    main()
