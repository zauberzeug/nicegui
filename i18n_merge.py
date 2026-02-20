#!/usr/bin/env python3
"""Merge translated JSON batch files back into website/translate.csv."""
import csv
import json
from pathlib import Path

CSV_FILE = Path('website/translate.csv')
BATCH_DIR = Path('/tmp/i18n_batches')

# Load all translated batches
translations: dict[str, str] = {}
for out_file in sorted(BATCH_DIR.glob('batch_*_out.json')):
    data = json.loads(out_file.read_text(encoding='utf-8'))
    translations.update(data)

print(f'Loaded {len(translations)} translations from batch output files')

# Read CSV
with CSV_FILE.open(encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

# Apply translations
applied = 0
for row in rows:
    en = row.get('en', '')
    if en in translations and not row.get('zh-CN', '').strip():
        row['zh-CN'] = translations[en]
        applied += 1

# Write back
with CSV_FILE.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'Applied {applied} translations to {CSV_FILE}')
still_missing = sum(1 for r in rows if not r.get('zh-CN', '').strip())
print(f'Still missing: {still_missing}/{len(rows)}')
