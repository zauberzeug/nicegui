#!/usr/bin/env python3
"""Merge translated JSON batch files back into the per-language CSV.

Each language is stored in a separate CSV file linked by SHA-256 hash of the English text.

Usage:
    python i18n_merge.py                    # merge into zh-CN
    python i18n_merge.py --language ja       # merge into Japanese
"""
import argparse
import csv
import json
from pathlib import Path

TRANSLATIONS_DIR = Path('website/translations')
BATCH_DIR = Path('/tmp/i18n_batches')


def main() -> None:
    parser = argparse.ArgumentParser(description='Merge translated batch files into language CSV.')
    parser.add_argument('--language', default='zh-CN', help='Target language code (default: zh-CN)')
    args = parser.parse_args()

    # Load all translated batches
    translations: dict[str, str] = {}
    for out_file in sorted(BATCH_DIR.glob('batch_*_out.json')):
        data = json.loads(out_file.read_text(encoding='utf-8'))
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and 'sha256' in item and 'text' in item:
                    translations[item['sha256']] = item['text']
        elif isinstance(data, dict):
            translations.update(data)

    print(f'Loaded {len(translations)} translations from batch output files')

    # Read English entries for ordering
    en_file = TRANSLATIONS_DIR / 'en.csv'
    with en_file.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        en_entries = [(row['sha256'], row['text']) for row in reader if row.get('sha256')]

    # Read existing language CSV
    lang_file = TRANSLATIONS_DIR / f'{args.language}.csv'
    existing: dict[str, str] = {}
    if lang_file.exists():
        with lang_file.open(encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            existing = {row['sha256']: row.get('text', '') for row in reader if row.get('sha256')}

    # Apply translations (only to empty cells)
    applied = 0
    for h, translation in translations.items():
        if h in {e[0] for e in en_entries} and not existing.get(h, '').strip():
            existing[h] = translation
            applied += 1

    # Write back
    with lang_file.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['sha256', 'text'], quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for h, _ in sorted(en_entries, key=lambda r: r[0]):
            writer.writerow({'sha256': h, 'text': existing.get(h, '')})

    print(f'Applied {applied} translations to {lang_file}')
    still_missing = sum(1 for h, _ in en_entries if not existing.get(h, '').strip())
    print(f'Still missing: {still_missing}/{len(en_entries)}')


if __name__ == '__main__':
    main()
