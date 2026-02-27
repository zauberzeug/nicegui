#!/usr/bin/env python3
"""Validate that all t() translation keys have entries in every language file.

Parses Python source files using the AST to extract string arguments passed to
``t()``, then checks each ``website/translations/<lang>.json`` for coverage.

Exit code 0 means all keys are present; exit code 1 lists the gaps.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

WEBSITE_DIR = Path(__file__).parent
TRANSLATIONS_DIR = WEBSITE_DIR / 'translations'
# Files that import and use t() from i18n
SEARCH_DIRS = [WEBSITE_DIR]


def _extract_t_keys(filepath: Path) -> list[tuple[int, str]]:
    """Return ``(lineno, key)`` pairs for every ``t('...')`` call in *filepath*."""
    source = filepath.read_text(encoding='utf-8')
    try:
        tree = ast.parse(source, filename=str(filepath))
    except SyntaxError:
        return []

    results: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == 't'
            and node.args
        ):
            arg = node.args[0]
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                results.append((node.lineno, arg.value))
            elif isinstance(arg, ast.JoinedStr):
                pass  # f-string - skip (shouldn't be used as translation key)
    return results


def main() -> int:
    # Collect all t() keys from Python source
    all_keys: dict[str, list[tuple[Path, int]]] = {}
    for search_dir in SEARCH_DIRS:
        for py_file in sorted(search_dir.rglob('*.py')):
            if py_file.name in {'i18n.py', 'check_translations.py'}:
                continue
            for lineno, key in _extract_t_keys(py_file):
                all_keys.setdefault(key, []).append((py_file, lineno))

    if not all_keys:
        print('No t() keys found - nothing to check.')
        return 0

    # Load translation files
    lang_files = sorted(TRANSLATIONS_DIR.glob('*.json'))
    if not lang_files:
        print(f'No translation files found in {TRANSLATIONS_DIR}')
        return 1

    errors: list[str] = []
    for lang_file in lang_files:
        lang = lang_file.stem
        translations = json.loads(lang_file.read_text(encoding='utf-8'))
        translated_keys = set(translations.keys())

        missing = sorted(set(all_keys) - translated_keys)
        if missing:
            errors.append(f'\n  {lang}.json is missing {len(missing)} key(s):')
            for key in missing:
                locations = all_keys[key]
                loc = locations[0]
                short_key = key[:70] + '...' if len(key) > 70 else key
                errors.append(f'    {loc[0].relative_to(WEBSITE_DIR)}:{loc[1]}  {short_key!r}')

        extra = sorted(translated_keys - set(all_keys))
        if extra:
            errors.append(f'\n  {lang}.json has {len(extra)} unused key(s):')
            for key in extra:
                short_key = key[:70] + '...' if len(key) > 70 else key
                errors.append(f'    {short_key!r}')

    if errors:
        print(f'Translation key mismatches found ({len(all_keys)} keys from source):')
        for line in errors:
            print(line)
        return 1

    print(f'All {len(all_keys)} translation keys present in {len(lang_files)} language file(s).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
