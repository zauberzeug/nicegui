#!/usr/bin/env python3
"""Check website/translate.csv for missing translations.

Usage:
    python i18n_check.py              # report missing, exit 0
    python i18n_check.py --strict     # exit 1 if any missing
    python i18n_check.py --language de # check only German
    python i18n_check.py --fix        # auto-correct untranslatable keys
"""
import argparse
import csv
import re
import sys
from pathlib import Path

CSV_FILE = Path(__file__).parent / 'website' / 'translate.csv'

# Matches API identifiers that must NOT be translated:
#   ui.*button*          (bold markdown API name)
#   ui.button            (plain API name)
#   ui.navigate.to       (dotted API name)
#   ui.navigate.to (formerly ui.open)  (with parenthetical note)
_API_ID_RE = re.compile(
    r'^ui\.'
    r'(?:'
    r'\*[a-z_]+\*'            # ui.*xxx*
    r'|'
    r'[a-z_]+(?:\.[a-z_]+)*'  # ui.xxx or ui.xxx.yyy
    r')'
    r'(?:\s*\(.*\))?$'        # optional trailing (...)
)


def is_untranslatable(english: str) -> bool:
    """Return True if the English key is an API identifier that must not be translated."""
    return bool(_API_ID_RE.match(english))


def main() -> None:
    parser = argparse.ArgumentParser(description='Check translation CSV for completeness.')
    parser.add_argument('--strict', action='store_true', help='Exit with code 1 if any translations are missing')
    parser.add_argument('--language', action='append', default=[], help='Check only specific language(s)')
    parser.add_argument('--fix', action='store_true', help='Auto-correct untranslatable API identifiers in-place')
    args = parser.parse_args()

    if not CSV_FILE.exists():
        print(f'Error: {CSV_FILE} does not exist. Run i18n_bootstrap.py first.')
        sys.exit(1)

    with CSV_FILE.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            print('Error: CSV has no headers.')
            sys.exit(1)

        fieldnames = list(reader.fieldnames)
        all_languages = [lang for lang in fieldnames if lang != 'en']
        check_languages = args.language if args.language else all_languages

        for lang in check_languages:
            if lang not in fieldnames:
                print(f'Error: Language "{lang}" not found in CSV. Available: {", ".join(all_languages)}')
                sys.exit(1)

        rows = list(reader)

    # Check and optionally fix untranslatable API identifiers
    fix_count = 0
    bad_rows: list[tuple[str, str, str]] = []  # (english, lang, translation)
    for row in rows:
        english = row['en']
        if not is_untranslatable(english):
            continue
        for lang in all_languages:
            translation = row.get(lang, '').strip()
            if translation and translation != english:
                bad_rows.append((english, lang, translation))
                if args.fix:
                    row[lang] = english
                    fix_count += 1

    if bad_rows:
        print(f'\nAPI identifiers that should not be translated: {len(bad_rows)} violation(s)')
        for english, lang, translation in bad_rows[:20]:
            print(f'  {lang}: "{english}" was translated as "{translation}"')
        if len(bad_rows) > 20:
            print(f'  ... and {len(bad_rows) - 20} more')

    if args.fix and fix_count:
        with CSV_FILE.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
        print(f'\nFixed {fix_count} untranslatable API identifier(s) in {CSV_FILE}')

    # Check for missing translations
    total = len(rows)
    any_missing = False

    for lang in check_languages:
        missing = [row['en'] for row in rows if not row.get(lang, '').strip()]
        if missing:
            any_missing = True
            print(f'\n{lang}: {len(missing)}/{total} translations missing')
            for english in missing[:10]:
                preview = english[:60].replace('\n', ' ').strip()
                print(f'  - "{preview}{"..." if len(english) > 60 else ""}"')
            if len(missing) > 10:
                print(f'  ... and {len(missing) - 10} more')
        else:
            print(f'{lang}: all {total} translations present')

    if args.strict and (any_missing or bad_rows):
        sys.exit(1)


if __name__ == '__main__':
    main()
