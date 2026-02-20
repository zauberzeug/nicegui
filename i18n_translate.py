#!/usr/bin/env python3
"""Translate missing zh-CN strings using a local LM Studio API (OpenAI-compatible).

Batches multiple strings per API call to maximize throughput with large context windows
(up to 262144 tokens). Falls back to single-string translation for failed batches.

Usage:
    python i18n_translate.py                          # translate all missing
    python i18n_translate.py --workers 4              # parallel batch requests
    python i18n_translate.py --dry-run                # preview without calling API
    python i18n_translate.py --api-url http://host:1234  # custom API URL
    python i18n_translate.py --batch-size 50          # strings per batch (0 = auto)
    python i18n_translate.py --no-batch               # one string at a time (old behavior)
"""
import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

CSV_FILE = Path(__file__).parent / 'website' / 'translate.csv'
DEFAULT_API_URL = 'http://host.docker.internal:1234'
TARGET_LANG = 'zh-CN'
SAVE_EVERY = 1  # save CSV every N translations

# Context budget: 262144 tokens total. Reserve half for output, some for system prompt.
MAX_CONTEXT_TOKENS = 262144
INPUT_TOKEN_BUDGET = 500  # conservative budget for input strings per batch
CHARS_PER_TOKEN = 4  # rough estimate for mixed English/markdown content

SYSTEM_PROMPT = (
    '你是一位专业的软件文档翻译员。将英文翻译成简体中文（zh-CN）。\n'  # noqa: RUF001
    '规则：\n'  # noqa: RUF001
    '- 完整保留所有 markdown 格式、HTML 标签、URL、代码块和行内代码\n'
    '- 完整保留原文的前后空白和缩进\n'
    '- 完整保留原文的换行\n'
    '- 不要翻译代码、变量名称、URL 或品牌名称（NiceGUI、Quasar、Vue、FastAPI 等）\n'  # noqa: RUF001
    '- 不要翻译反引号内的文字（`...`）\n'  # noqa: RUF001
    '- 使用中国大陆标准简体中文\n'
    '- 只输出翻译结果，不要加任何说明或备注。'  # noqa: RUF001
)

BATCH_SYSTEM_PROMPT = (
    '你是一位专业的软件文档翻译员。将英文翻译成简体中文（zh-CN）。\n'  # noqa: RUF001
    '规则：\n'  # noqa: RUF001
    '- 完整保留所有 markdown 格式、HTML 标签、URL、代码块和行内代码\n'
    '- 完整保留原文的前后空白和缩进\n'
    '- 完整保留原文的换行\n'
    '- 不要翻译代码、变量名称、URL 或品牌名称（NiceGUI、Quasar、Vue、FastAPI 等）\n'  # noqa: RUF001
    '- 不要翻译反引号内的文字（`...`）\n'  # noqa: RUF001
    '- 使用中国大陆标准简体中文\n\n'
    '你会收到多个编号的字符串。请用完全相同的编号格式回复每一个翻译。\n'
    '格式：每个翻译以 「[数字]」 开头，后接一个空格，然后是翻译内容。\n'  # noqa: RUF001
    '翻译之间用空行分隔。不要加任何说明或备注。\n'
    '示例输入：\n'  # noqa: RUF001
    '[1] Hello World\n\n'
    '[2] Click here\n\n'
    '示例输出：\n'  # noqa: RUF001
    '[1] 你好世界\n\n'
    '[2] 点击这里'
)


def estimate_tokens(text: str) -> int:
    """Rough token count estimate."""
    return len(text) // CHARS_PER_TOKEN + 1


def call_lm_studio(api_url: str, messages: list[dict], max_tokens: int,
                   temperature: float = 0.3) -> str:
    """Send a chat completion request to the LM Studio API."""
    payload = json.dumps({
        'messages': messages,
        'temperature': temperature,
        'max_tokens': max_tokens,
        'stream': False,
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{api_url}/v1/chat/completions',
        data=payload,
        headers={'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    return data['choices'][0]['message']['content'].strip()


def translate_single(api_url: str, english: str) -> str:
    """Translate a single string via the LM Studio API."""
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': f'请翻译成简体中文：\n\n{english}'},  # noqa: RUF001
    ]
    max_tokens = max(4096, estimate_tokens(english) * 3)
    return call_lm_studio(api_url, messages, max_tokens)


def translate_batch(api_url: str, items: list[tuple[int, str]]) -> dict[int, str]:
    """Translate a batch of numbered strings. Returns {index: translation}."""
    # Build numbered input
    parts = []
    for idx, english in items:
        parts.append(f'[{idx}] {english}')
    batch_input = '\n\n'.join(parts)

    messages = [
        {'role': 'system', 'content': BATCH_SYSTEM_PROMPT},
        {'role': 'user', 'content': f'请翻译以下编号字符串成简体中文：\n\n{batch_input}'},  # noqa: RUF001
    ]
    total_input_chars = sum(len(en) for _, en in items)
    toplevel_max_tokens = max(8192, estimate_tokens(total_input_chars * 3)
                              if isinstance(total_input_chars, str) else total_input_chars * 3 // CHARS_PER_TOKEN)
    # Cap at context limit minus input estimate
    toplevel_max_tokens = min(toplevel_max_tokens, MAX_CONTEXT_TOKENS // 2)

    response = call_lm_studio(api_url, messages, toplevel_max_tokens)
    return parse_batch_response(response, [idx for idx, _ in items])


def parse_batch_response(response: str, expected_indices: list[int]) -> dict[int, str]:
    """Parse a numbered batch response into {index: translation}."""
    results: dict[int, str] = {}
    # Split on [N] markers at the start of a line
    pattern = re.compile(r'^\[(\d+)\]\s', re.MULTILINE)
    matches = list(pattern.finditer(response))

    for i, match in enumerate(matches):
        idx = int(match.group(1))
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(response)
        translation = response[start:end].strip()
        if translation and idx in expected_indices:
            results[idx] = translation

    return results


def create_batches(items: list[tuple[int, int, str]], batch_size: int) -> list[list[tuple[int, int, str]]]:
    """Group items into batches respecting both count and token budget."""
    batches: list[list[tuple[int, int, str]]] = []
    current_batch: list[tuple[int, int, str]] = []
    current_tokens = 0

    for item in items:
        _seq, _csv_idx, english = item
        item_tokens = estimate_tokens(english) + 10  # overhead for [N] marker
        # Start new batch if adding this item would exceed budget or count
        if current_batch and (len(current_batch) >= batch_size or current_tokens + item_tokens > INPUT_TOKEN_BUDGET):
            batches.append(current_batch)
            current_batch = []
            current_tokens = 0
        current_batch.append(item)
        current_tokens += item_tokens

    if current_batch:
        batches.append(current_batch)
    return batches


def process_batch(batch: list[tuple[int, int, str]], api_url: str) -> list[tuple[int, str | None, str | None]]:
    """Translate a batch. Returns [(csv_idx, translation, error), ...]."""
    numbered_items = [(i + 1, english) for i, (_, _, english) in enumerate(batch)]

    try:
        translations = translate_batch(api_url, numbered_items)
    except Exception as e:
        # Entire batch failed - return errors for all
        return [(csv_idx, None, f'batch error: {e}') for _, csv_idx, _ in batch]

    results = []
    failed_items = []
    for seq_num, (_, csv_idx, english) in enumerate(batch, 1):
        if seq_num in translations and translations[seq_num].strip():
            results.append((csv_idx, translations[seq_num], None))
        else:
            failed_items.append((csv_idx, english))

    # Retry failed items individually
    for csv_idx, english in failed_items:
        try:
            translation = translate_single(api_url, english)
            if translation.strip():
                results.append((csv_idx, translation, None))
            else:
                results.append((csv_idx, None, 'empty response'))
        except Exception as e:
            results.append((csv_idx, None, str(e)))

    return results


def translate_one(args: tuple[int, int, str, str]) -> tuple[int, int, str | None, str | None]:
    """Translate a single string (no-batch mode). Returns (seq, csv_idx, translation, error)."""
    seq, csv_idx, english, api_url = args
    try:
        translation = translate_single(api_url, english)
        if not translation.strip():
            return seq, csv_idx, None, 'empty response'
        return seq, csv_idx, translation, None
    except Exception as e:
        return seq, csv_idx, None, str(e)


def auto_batch_size(items: list[tuple[int, int, str]]) -> int:
    """Pick a batch size based on average string length."""
    if not items:
        return 1
    avg_tokens = sum(estimate_tokens(en) for _, _, en in items) / len(items)
    # Aim to use ~80% of input budget per batch
    target = int(INPUT_TOKEN_BUDGET * 0.8 / max(avg_tokens + 10, 1))
    return max(1, min(target, 200))  # cap at 200 strings per batch


def main() -> None:
    parser = argparse.ArgumentParser(description='Translate missing strings using LM Studio.')
    parser.add_argument('--api-url', default=DEFAULT_API_URL, help=f'LM Studio API URL (default: {DEFAULT_API_URL})')
    parser.add_argument('--workers', type=int, default=2, help='Concurrent translation requests (default: 2)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be translated without calling API')
    parser.add_argument('--start-from', type=int, default=0, help='Skip first N missing strings (for resuming)')
    parser.add_argument('--limit', type=int, default=0, help='Translate at most N strings (0 = all)')
    parser.add_argument('--batch-size', type=int, default=0,
                        help='Strings per API call (0 = auto, based on avg length)')
    parser.add_argument('--no-batch', action='store_true', help='Disable batching (one string per API call)')
    args = parser.parse_args()

    if not CSV_FILE.exists():
        print(f'Error: {CSV_FILE} not found. Run i18n_bootstrap.py first.')
        sys.exit(1)

    # Read CSV
    with CSV_FILE.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if TARGET_LANG not in fieldnames:
        print(f'Error: {TARGET_LANG} column not in CSV')
        sys.exit(1)

    # Find missing translations
    missing_indices = [i for i, row in enumerate(rows) if not row.get(TARGET_LANG, '').strip()]
    total_missing = len(missing_indices)
    print(f'Found {total_missing}/{len(rows)} missing {TARGET_LANG} translations')

    if args.start_from > 0:
        missing_indices = missing_indices[args.start_from:]
        print(f'Skipping first {args.start_from}, {len(missing_indices)} remaining')

    if args.limit > 0:
        missing_indices = missing_indices[:args.limit]
        print(f'Limiting to {len(missing_indices)} strings')

    if not missing_indices:
        print('Nothing to translate!')
        return

    # Build work items: (seq, csv_idx, english)
    items = [(seq, csv_idx, rows[csv_idx]['en']) for seq, csv_idx in enumerate(missing_indices)]

    if args.dry_run:
        batch_size = 1 if args.no_batch else (args.batch_size or auto_batch_size(items))
        mode = 'single-string' if args.no_batch else f'batch (size ~{batch_size})'
        print(f'\nDry run: would translate {len(items)} strings, mode={mode}, workers={args.workers}')
        for _, csv_idx, english in items[:5]:
            preview = english[:80].replace('\n', '\\n')
            print(f'  [{csv_idx}] {preview}...')
        if len(items) > 5:
            print(f'  ... and {len(items) - 5} more')
        return

    # Check API connectivity
    print(f'\nChecking API at {args.api_url}...')
    try:
        req = urllib.request.Request(f'{args.api_url}/v1/models')
        with urllib.request.urlopen(req, timeout=10) as resp:
            models = json.loads(resp.read().decode('utf-8'))
            model_names = [m.get('id', '?') for m in models.get('data', [])]
            print(f'Connected! Available models: {", ".join(model_names)}')
    except Exception as e:
        print(f'Error: Cannot connect to LM Studio at {args.api_url}: {e}')
        print('Make sure LM Studio is running and the port is forwarded.')
        sys.exit(1)

    def save_csv() -> None:
        with CSV_FILE.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    translated_count = 0
    failed_count = 0
    total = len(items)
    t_start = time.time()

    if args.no_batch:
        # Original single-string mode
        print(f'\nTranslating {total} strings one-at-a-time with {args.workers} workers...\n')
        work = [(seq, csv_idx, english, args.api_url) for seq, csv_idx, english in items]
        try:
            with ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = {executor.submit(translate_one, w): w for w in work}
                for future in as_completed(futures):
                    _, csv_idx, translation, error = future.result()
                    en_preview = rows[csv_idx]['en'][:60].replace('\n', '\\n')
                    if translation:
                        rows[csv_idx][TARGET_LANG] = translation
                        translated_count += 1
                        zh_preview = translation[:60].replace('\n', '\\n')
                        elapsed = time.time() - t_start
                        rate = translated_count / elapsed * 60 if elapsed > 0 else 0
                        print(f'  [{translated_count}/{total}] ({rate:.0f}/min) "{en_preview}..."')
                        print(f'    -> "{zh_preview}..."')
                    else:
                        failed_count += 1
                        print(f'  FAILED [{failed_count}] "{en_preview}...": {error}')
                    if translated_count % SAVE_EVERY == 0 and translated_count > 0:
                        print(f'  -- Saving progress ({translated_count} done) --')
                        save_csv()
        except KeyboardInterrupt:
            print('\n\nInterrupted! Saving progress...')
    else:
        # Batch mode
        batch_size = args.batch_size or auto_batch_size(items)
        batches = create_batches(items, batch_size)
        print(f'\nTranslating {total} strings in {len(batches)} batches '
              f'(~{batch_size} strings/batch) with {args.workers} workers...\n')

        try:
            with ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = {
                    executor.submit(process_batch, batch, args.api_url): batch
                    for batch in batches
                }
                for future in as_completed(futures):
                    results = future.result()
                    for csv_idx, translation, error in results:
                        en_preview = rows[csv_idx]['en'][:60].replace('\n', '\\n')
                        if translation:
                            rows[csv_idx][TARGET_LANG] = translation
                            translated_count += 1
                            zh_preview = translation[:60].replace('\n', '\\n')
                            elapsed = time.time() - t_start
                            rate = translated_count / elapsed * 60 if elapsed > 0 else 0
                            print(f'  [{translated_count}/{total}] ({rate:.0f}/min) "{en_preview}..."')
                            print(f'    -> "{zh_preview}..."')
                        else:
                            failed_count += 1
                            print(f'  FAILED [{failed_count}] "{en_preview}...": {error}')

                    if translated_count % SAVE_EVERY == 0 and translated_count > 0:
                        print(f'  -- Saving progress ({translated_count} done) --')
                        save_csv()
        except KeyboardInterrupt:
            print('\n\nInterrupted! Saving progress...')

    # Final save
    print(f'\nSaving final results to {CSV_FILE}...')
    save_csv()

    elapsed = time.time() - t_start
    still_missing = sum(1 for r in rows if not r.get(TARGET_LANG, '').strip())
    print(f'\nDone in {elapsed:.0f}s! Translated: {translated_count}, Failed: {failed_count}')
    print(f'Still missing: {still_missing}/{len(rows)}')


if __name__ == '__main__':
    main()
