#!/usr/bin/env python3
"""Extract missing translations into numbered JSON batch files.

Each language is stored in a separate CSV file linked by SHA-256 hash of the English text.

Usage:
    python i18n_batch_extract.py                    # extract missing zh-CN
    python i18n_batch_extract.py --language ja       # extract missing Japanese
"""
import argparse
import csv
import json
import math
from pathlib import Path

TRANSLATIONS_DIR = Path('website/translations')
BATCH_DIR = Path('/tmp/i18n_batches')
BATCH_SIZE = 50  # strings per batch


def main() -> None:
    parser = argparse.ArgumentParser(description='Extract missing translations into batch files.')
    parser.add_argument('--language', default='zh-CN', help='Target language code (default: zh-CN)')
    args = parser.parse_args()

    BATCH_DIR.mkdir(exist_ok=True)

    # Read English entries
    en_file = TRANSLATIONS_DIR / 'en.csv'
    with en_file.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        en_entries = [(row['sha256'], row['text']) for row in reader if row.get('sha256') and row.get('text')]

    hash_to_english = {h: en for h, en in en_entries}

    # Read existing translations
    lang_file = TRANSLATIONS_DIR / f'{args.language}.csv'
    existing: dict[str, str] = {}
    if lang_file.exists():
        with lang_file.open(encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            existing = {row['sha256']: row.get('text', '') for row in reader if row.get('sha256')}

    # Find missing
    missing = [(h, hash_to_english[h]) for h, _ in en_entries if not existing.get(h, '').strip()]
    num_batches = math.ceil(len(missing) / BATCH_SIZE)

    for i in range(num_batches):
        batch = missing[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
        # Write as list of {sha256, text} objects
        batch_data = [{'sha256': h, 'text': en} for h, en in batch]
        batch_file = BATCH_DIR / f'batch_{i:03d}.json'
        batch_file.write_text(json.dumps(batch_data, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'Wrote {num_batches} batch files to {BATCH_DIR}/ ({len(missing)} strings, {BATCH_SIZE}/batch)')
    print(f'Language: {args.language}')


if __name__ == '__main__':
    main()
