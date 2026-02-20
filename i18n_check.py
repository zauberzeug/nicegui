#!/usr/bin/env python3
"""Check website/translate.csv for missing translations.

Usage:
    python i18n_check.py              # report missing, exit 0
    python i18n_check.py --strict     # exit 1 if any missing
    python i18n_check.py --language de # check only German
"""
import argparse
import csv
import sys
from pathlib import Path

CSV_FILE = Path(__file__).parent / 'website' / 'translate.csv'


def main() -> None:
    parser = argparse.ArgumentParser(description='Check translation CSV for completeness.')
    parser.add_argument('--strict', action='store_true', help='Exit with code 1 if any translations are missing')
    parser.add_argument('--language', action='append', default=[], help='Check only specific language(s)')
    args = parser.parse_args()

    if not CSV_FILE.exists():
        print(f'Error: {CSV_FILE} does not exist. Run i18n_bootstrap.py first.')
        sys.exit(1)

    with CSV_FILE.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            print('Error: CSV has no headers.')
            sys.exit(1)

        all_languages = [lang for lang in reader.fieldnames if lang != 'en']
        check_languages = args.language if args.language else all_languages

        for lang in check_languages:
            if lang not in reader.fieldnames:
                print(f'Error: Language "{lang}" not found in CSV. Available: {", ".join(all_languages)}')
                sys.exit(1)

        rows = list(reader)

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

    if any_missing and args.strict:
        sys.exit(1)


if __name__ == '__main__':
    main()
