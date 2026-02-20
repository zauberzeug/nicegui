#!/usr/bin/env python3
"""Bootstrap and update website/translate.csv from t() calls, documentation registry, and examples.

Extracts translatable strings from three sources:
1. Static: AST parsing of t() calls in website/**/*.py
2. Runtime: importing the documentation registry to enumerate page titles, subtitles, and part descriptions
3. Static: titles and descriptions from examples/*/README.md files

Usage:
    python i18n_bootstrap.py                    # sync CSV with code
    python i18n_bootstrap.py --add-language de   # add a new language column
"""
import argparse
import ast
import csv
import inspect
import re
import sys
from pathlib import Path

WEBSITE_DIR = Path(__file__).parent / 'website'
EXAMPLES_DIR = Path(__file__).parent / 'examples'
CSV_FILE = WEBSITE_DIR / 'translate.csv'


TRANSLATING_FUNCTIONS = {'t', 'subheading', '_main_page_demo'}


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


def read_csv(path: Path) -> tuple[list[str], dict[str, dict[str, str]]]:
    """Read existing CSV and return (languages, {english: {lang: translation}})."""
    if not path.exists():
        return ['en'], {}
    with path.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return ['en'], {}
        languages = list(reader.fieldnames)
        rows: dict[str, dict[str, str]] = {}
        for row in reader:
            english = row.get('en', '')
            if english:
                rows[english] = {lang: row.get(lang, '') for lang in languages if lang != 'en'}
        return languages, rows


def write_csv(path: Path, languages: list[str], rows: dict[str, dict[str, str]]) -> None:
    """Write the CSV file sorted by English text."""
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=languages)
        writer.writeheader()
        for english in sorted(rows, key=lambda s: (s.casefold(), s)):
            row = {'en': english}
            row.update(rows[english])
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description='Bootstrap/update website translation CSV.')
    parser.add_argument('--add-language', action='append', default=[], help='Add a new language column')
    parser.add_argument('--no-registry', action='store_true', help='Skip documentation registry enumeration')
    args = parser.parse_args()

    code_strings = extract_t_strings(WEBSITE_DIR)
    example_strings = extract_example_strings(EXAMPLES_DIR)
    if not args.no_registry:
        doc_strings = extract_doc_strings()
        all_strings = code_strings | doc_strings | example_strings
        print(f'Found {len(code_strings)} t() strings + {len(doc_strings)} doc registry strings + {len(example_strings)} example strings')
    else:
        all_strings = code_strings | example_strings
        print(f'Found {len(code_strings)} t() strings + {len(example_strings)} example strings (registry skipped)')

    languages, existing_rows = read_csv(CSV_FILE)

    for lang in args.add_language:
        if lang not in languages:
            languages.append(lang)

    if 'en' not in languages:
        languages.insert(0, 'en')

    new_rows: dict[str, dict[str, str]] = {}
    added = 0
    removed = 0
    for english in all_strings:
        if english in existing_rows:
            new_rows[english] = existing_rows[english]
        else:
            new_rows[english] = {lang: '' for lang in languages if lang != 'en'}
            added += 1

    for english in existing_rows:
        if english not in all_strings:
            removed += 1

    for _english, translations in new_rows.items():
        for lang in languages:
            if lang != 'en' and lang not in translations:
                translations[lang] = ''

    write_csv(CSV_FILE, languages, new_rows)

    total = len(new_rows)
    print(f'Wrote {CSV_FILE}: {total} strings, {added} added, {removed} removed, {len(languages)} languages')


if __name__ == '__main__':
    main()
