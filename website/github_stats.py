import json
from pathlib import Path

STATS = json.loads((Path(__file__).parent / 'github_stats.json').read_text(encoding='utf-8'))
STARS_STRING = f'{STATS["stars"] // 1000}k+'
