#!/usr/bin/env python3
"""Extract missing translations into numbered JSON batch files."""
import csv
import json
import math
from pathlib import Path

CSV_FILE = Path('website/translate.csv')
BATCH_DIR = Path('/tmp/i18n_batches')
BATCH_SIZE = 50  # strings per batch

BATCH_DIR.mkdir(exist_ok=True)

with CSV_FILE.open(encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

missing = [r['en'] for r in rows if not r.get('zh-CN', '').strip()]
num_batches = math.ceil(len(missing) / BATCH_SIZE)

for i in range(num_batches):
    batch = missing[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
    batch_file = BATCH_DIR / f'batch_{i:03d}.json'
    batch_file.write_text(json.dumps(batch, ensure_ascii=False, indent=2), encoding='utf-8')

print(f'Wrote {num_batches} batch files to {BATCH_DIR}/ ({len(missing)} strings, {BATCH_SIZE}/batch)')
