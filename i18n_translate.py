#!/usr/bin/env python3
"""Translate missing strings for a target language using a local LM Studio API (OpenAI-compatible).

Batches multiple strings per API call to maximize throughput with large context windows
(up to 262144 tokens). Falls back to single-string translation for failed batches.

Each language is stored in a separate CSV file linked by SHA-256 hash of the English text.

Usage:
    python i18n_translate.py                               # translate missing zh-CN
    python i18n_translate.py --language ja                  # translate missing Japanese
    python i18n_translate.py --language ja --model gemma-3-4b  # use specific model
    python i18n_translate.py --workers 4                    # parallel batch requests
    python i18n_translate.py --dry-run                      # preview without calling API
    python i18n_translate.py --api-url http://host:1234     # custom API URL
    python i18n_translate.py --batch-size 50                # strings per batch (0 = auto)
    python i18n_translate.py --no-batch                     # one string at a time
"""
import argparse
import csv
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

TRANSLATIONS_DIR = Path(__file__).parent / 'website' / 'translations'
DEFAULT_API_URL = 'http://host.docker.internal:1234'
SAVE_INTERVAL = 15  # save CSV at most every N seconds

# Context budget: 262144 tokens total. Reserve half for output, some for system prompt.
MAX_CONTEXT_TOKENS = 262144
INPUT_TOKEN_BUDGET = 500  # conservative budget for input strings per batch
CHARS_PER_TOKEN = 4  # rough estimate for mixed English/markdown content

# Language-specific system prompts (without reference)
_SYSTEM_PROMPTS_BASE: dict[str, str] = {
    'zh-CN': (
        '你是一位专业的软件文档翻译员。将英文翻译成简体中文（zh-CN）。\n'  # noqa: RUF001
        '规则：\n'  # noqa: RUF001
        '- 完整保留所有 markdown 格式、HTML 标签、URL、代码块和行内代码\n'
        '- 完整保留原文的前后空白和缩进\n'
        '- 完整保留原文的换行\n'
        '- 不要翻译代码、变量名称、URL 或品牌名称（NiceGUI、Quasar、Vue、FastAPI 等）\n'  # noqa: RUF001
        '- 不要翻译反引号内的文字（`...`）\n'  # noqa: RUF001
        '- 使用中国大陆标准简体中文\n'
        '- 只输出翻译结果，不要加任何说明或备注。'  # noqa: RUF001
    ),
    'ja': (
        'あなたはプロのソフトウェアドキュメント翻訳者です。英語を日本語に翻訳してください。\n'
        'ルール：\n'  # noqa: RUF001
        '- すべてのmarkdown書式、HTMLタグ、URL、コードブロック、インラインコードを完全に保持する\n'
        '- 原文の前後の空白とインデントを完全に保持する\n'
        '- 原文の改行を完全に保持する\n'
        '- コード、変数名、URL、ブランド名（NiceGUI、Quasar、Vue、FastAPI等）は翻訳しない\n'  # noqa: RUF001
        '- バッククォート内のテキスト（`...`）は翻訳しない\n'  # noqa: RUF001
        '- 自然な日本語を使用する\n'
        '- 翻訳結果のみを出力し、説明や注釈は付けないこと。'
    ),
    'ko': (
        '당신은 전문 소프트웨어 문서 번역가입니다. 영어를 한국어로 번역해 주세요.\n'
        '규칙:\n'
        '- 모든 markdown 서식, HTML 태그, URL, 코드 블록, 인라인 코드를 그대로 유지할 것\n'
        '- 원문의 앞뒤 공백과 들여쓰기를 그대로 유지할 것\n'
        '- 원문의 줄바꿈을 그대로 유지할 것\n'
        '- 코드, 변수명, URL, 브랜드명(NiceGUI, Quasar, Vue, FastAPI 등)은 번역하지 말 것\n'
        '- 백틱 안의 텍스트(`...`)는 번역하지 말 것\n'
        '- 자연스러운 한국어를 사용할 것\n'
        '- 번역 결과만 출력하고 설명이나 주석은 달지 말 것.'
    ),
}

# Reference-language hint appended when --reference-language is used
_REF_HINT: dict[str, str] = {
    'ja': '\n中国語(zh-CN)の参考訳が「REF:」で提供される場合があります。参考にしつつ、日本語で出力してください。',
    'ko': '\n참고 번역(REF:)이 제공될 수 있습니다. 참고하되 한국어로만 출력해 주세요.',
}
_REF_HINT_DEFAULT = '\nA reference translation (REF:) may be provided for each string. Use it as a hint but output only {lang_name}.'

_BATCH_SYSTEM_PROMPTS_BASE: dict[str, str] = {
    'zh-CN': (
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
    ),
    'ja': (
        'あなたはプロのソフトウェアドキュメント翻訳者です。英語を日本語に翻訳してください。\n'
        'ルール：\n'  # noqa: RUF001
        '- すべてのmarkdown書式、HTMLタグ、URL、コードブロック、インラインコードを完全に保持する\n'
        '- 原文の前後の空白とインデントを完全に保持する\n'
        '- 原文の改行を完全に保持する\n'
        '- コード、変数名、URL、ブランド名（NiceGUI、Quasar、Vue、FastAPI等）は翻訳しない\n'  # noqa: RUF001
        '- バッククォート内のテキスト（`...`）は翻訳しない\n'  # noqa: RUF001
        '- 自然な日本語を使用する\n\n'
        '番号付きの文字列が複数送られます。同じ番号形式で翻訳を返してください。\n'
        '形式：各翻訳は「[番号]」で始まり、スペースの後に翻訳内容を記述。\n'  # noqa: RUF001
        '翻訳の間は空行で区切ってください。説明や注釈は付けないこと。\n'
        '入力例：\n'  # noqa: RUF001
        '[1] Hello World\n\n'
        '[2] Click here\n\n'
        '出力例：\n'  # noqa: RUF001
        '[1] こんにちは世界\n\n'
        '[2] ここをクリック'
    ),
    'ko': (
        '당신은 전문 소프트웨어 문서 번역가입니다. 영어를 한국어로 번역해 주세요.\n'
        '규칙:\n'
        '- 모든 markdown 서식, HTML 태그, URL, 코드 블록, 인라인 코드를 그대로 유지할 것\n'
        '- 원문의 앞뒤 공백과 들여쓰기를 그대로 유지할 것\n'
        '- 원문의 줄바꿈을 그대로 유지할 것\n'
        '- 코드, 변수명, URL, 브랜드명(NiceGUI, Quasar, Vue, FastAPI 등)은 번역하지 말 것\n'
        '- 백틱 안의 텍스트(`...`)는 번역하지 말 것\n'
        '- 자연스러운 한국어를 사용할 것\n\n'
        '번호가 매겨진 여러 문자열이 전송됩니다. 동일한 번호 형식으로 번역을 반환해 주세요.\n'
        '형식: 각 번역은 [번호]로 시작하고 공백 뒤에 번역 내용을 작성합니다.\n'
        '번역 사이는 빈 줄로 구분합니다. 설명이나 주석은 달지 마세요.\n'
        '입력 예시:\n'
        '[1] Hello World\n\n'
        '[2] Click here\n\n'
        '출력 예시:\n'
        '[1] 안녕하세요 세계\n\n'
        '[2] 여기를 클릭하세요'
    ),
}

_BATCH_REF_HINT: dict[str, str] = {
    'ja': '\n各文字列には「EN:」(英語原文)と「REF:」(中文参考訳)があります。参考にしつつ、日本語のみを出力してください。',
    'ko': '\n각 문자열에는 EN(영어 원문)과 REF(참고 번역)가 있습니다. 참고하되 한국어만 출력해 주세요.',
}
_BATCH_REF_HINT_DEFAULT = '\nEach item has EN (English) and REF (reference translation). Use REF as a hint but output only {lang_name}.'

# Default fallback prompts for unknown languages
DEFAULT_SYSTEM_PROMPT = (
    'You are a professional software documentation translator. Translate English to {lang_name}.\n'
    'Rules:\n'
    '- Preserve all markdown formatting, HTML tags, URLs, code blocks and inline code\n'
    '- Preserve all leading/trailing whitespace and indentation\n'
    '- Preserve all newlines\n'
    '- Do NOT translate code, variable names, URLs or brand names (NiceGUI, Quasar, Vue, FastAPI etc.)\n'
    '- Do NOT translate text inside backticks (`...`)\n'
    '- Output only the translation, no explanations or notes.'
)

DEFAULT_BATCH_SYSTEM_PROMPT = (
    'You are a professional software documentation translator. Translate English to {lang_name}.\n'
    'Rules:\n'
    '- Preserve all markdown formatting, HTML tags, URLs, code blocks and inline code\n'
    '- Preserve all leading/trailing whitespace and indentation\n'
    '- Preserve all newlines\n'
    '- Do NOT translate code, variable names, URLs or brand names (NiceGUI, Quasar, Vue, FastAPI etc.)\n'
    '- Do NOT translate text inside backticks (`...`)\n\n'
    'You will receive multiple numbered strings. Reply with translations in the same numbered format.\n'
    'Format: each translation starts with [number] followed by a space, then the translation.\n'
    'Separate translations with blank lines. No explanations or notes.\n'
    'Example input:\n'
    '[1] Hello World\n\n'
    '[2] Click here\n\n'
    'Example output:\n'
    '[1] Translation of Hello World\n\n'
    '[2] Translation of Click here'
)

LANG_NAMES: dict[str, str] = {
    'zh-CN': 'Simplified Chinese (zh-CN)',
    'ja': 'Japanese',
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish',
    'ko': 'Korean',
    'pt': 'Portuguese',
    'ru': 'Russian',
}

# Translate instruction per language
TRANSLATE_INSTRUCTION: dict[str, str] = {
    'zh-CN': '请翻译成简体中文：\n\n',  # noqa: RUF001
    'ja': '日本語に翻訳してください：\n\n',  # noqa: RUF001
    'ko': '한국어로 번역해 주세요:\n\n',
}

BATCH_TRANSLATE_INSTRUCTION: dict[str, str] = {
    'zh-CN': '请翻译以下编号字符串成简体中文：\n\n',  # noqa: RUF001
    'ja': '以下の番号付き文字列を日本語に翻訳してください：\n\n',  # noqa: RUF001
    'ko': '다음 번호가 매겨진 문자열을 한국어로 번역해 주세요:\n\n',
}


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def get_system_prompt(lang: str, has_reference: bool = False) -> str:
    if lang in _SYSTEM_PROMPTS_BASE:
        prompt = _SYSTEM_PROMPTS_BASE[lang]
    else:
        lang_name = LANG_NAMES.get(lang, lang)
        prompt = DEFAULT_SYSTEM_PROMPT.format(lang_name=lang_name)
    if has_reference:
        hint = _REF_HINT.get(lang, _REF_HINT_DEFAULT.format(lang_name=LANG_NAMES.get(lang, lang)))
        prompt += hint
    return prompt


def get_batch_system_prompt(lang: str, has_reference: bool = False) -> str:
    if lang in _BATCH_SYSTEM_PROMPTS_BASE:
        prompt = _BATCH_SYSTEM_PROMPTS_BASE[lang]
    else:
        lang_name = LANG_NAMES.get(lang, lang)
        prompt = DEFAULT_BATCH_SYSTEM_PROMPT.format(lang_name=lang_name)
    if has_reference:
        hint = _BATCH_REF_HINT.get(lang, _BATCH_REF_HINT_DEFAULT.format(lang_name=LANG_NAMES.get(lang, lang)))
        prompt += hint
    return prompt


def get_translate_instruction(lang: str) -> str:
    if lang in TRANSLATE_INSTRUCTION:
        return TRANSLATE_INSTRUCTION[lang]
    lang_name = LANG_NAMES.get(lang, lang)
    return f'Translate to {lang_name}:\n\n'


def get_batch_translate_instruction(lang: str) -> str:
    if lang in BATCH_TRANSLATE_INSTRUCTION:
        return BATCH_TRANSLATE_INSTRUCTION[lang]
    lang_name = LANG_NAMES.get(lang, lang)
    return f'Translate the following numbered strings to {lang_name}:\n\n'


def estimate_tokens(text: str) -> int:
    """Rough token count estimate."""
    return len(text) // CHARS_PER_TOKEN + 1


def call_lm_studio(api_url: str, messages: list[dict], max_tokens: int,
                   temperature: float = 0.3, model: str | None = None) -> str:
    """Send a chat completion request to the LM Studio API."""
    payload: dict = {
        'messages': messages,
        'temperature': temperature,
        'max_tokens': max_tokens,
        'stream': False,
    }
    if model:
        payload['model'] = model

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        f'{api_url}/v1/chat/completions',
        data=data,
        headers={'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    return result['choices'][0]['message']['content'].strip()


def translate_single(api_url: str, english: str, lang: str, model: str | None = None,
                     reference: str | None = None) -> str:
    """Translate a single string via the LM Studio API."""
    instruction = get_translate_instruction(lang)
    if reference:
        content = f'{instruction}EN: {english}\n    REF: {reference}'
    else:
        content = f'{instruction}{english}'
    messages = [
        {'role': 'system', 'content': get_system_prompt(lang, has_reference=bool(reference))},
        {'role': 'user', 'content': content},
    ]
    max_tokens = max(4096, estimate_tokens(english) * 3)
    return call_lm_studio(api_url, messages, max_tokens, model=model)


def translate_batch(api_url: str, items: list[tuple[int, str]], lang: str,
                    model: str | None = None,
                    references: dict[int, str] | None = None) -> dict[int, str]:
    """Translate a batch of numbered strings. Returns {index: translation}."""
    parts = [f'[{idx}] {english}' for idx, english in items]
    batch_input = '\n\n'.join(parts)

    instruction = get_batch_translate_instruction(lang)
    messages = [
        {'role': 'system', 'content': get_batch_system_prompt(lang, has_reference=bool(references))},
    ]
    if references:
        ref_parts = [f'[{idx}] {references[idx]}' for idx, _ in items if idx in references]
        if ref_parts:
            messages.append({'role': 'user', 'content': 'Reference translations (zh-CN):\n\n' + '\n\n'.join(ref_parts)})
            messages.append({'role': 'assistant', 'content': 'Understood. I will use these as reference. Please provide the English strings to translate.'})
    messages.append({'role': 'user', 'content': f'{instruction}{batch_input}'})
    total_input_chars = sum(len(en) for _, en in items)
    toplevel_max_tokens = max(8192, total_input_chars * 3 // CHARS_PER_TOKEN)
    toplevel_max_tokens = min(toplevel_max_tokens, MAX_CONTEXT_TOKENS // 2)

    response = call_lm_studio(api_url, messages, toplevel_max_tokens, model=model)
    return parse_batch_response(response, [idx for idx, _ in items])


def parse_batch_response(response: str, expected_indices: list[int]) -> dict[int, str]:
    """Parse a numbered batch response into {index: translation}."""
    results: dict[int, str] = {}
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


def create_batches(items: list[tuple[int, str, str]], batch_size: int) -> list[list[tuple[int, str, str]]]:
    """Group items into batches respecting both count and token budget."""
    batches: list[list[tuple[int, str, str]]] = []
    current_batch: list[tuple[int, str, str]] = []
    current_tokens = 0

    for item in items:
        _seq, _hash, english = item
        item_tokens = estimate_tokens(english) + 10
        if current_batch and (len(current_batch) >= batch_size or current_tokens + item_tokens > INPUT_TOKEN_BUDGET):
            batches.append(current_batch)
            current_batch = []
            current_tokens = 0
        current_batch.append(item)
        current_tokens += item_tokens

    if current_batch:
        batches.append(current_batch)
    return batches


def process_batch(batch: list[tuple[int, str, str]], api_url: str, lang: str,
                  model: str | None = None,
                  ref_translations: dict[str, str] | None = None) -> list[tuple[str, str | None, str | None]]:
    """Translate a batch. Returns [(hash, translation, error), ...]."""
    numbered_items = [(i + 1, english) for i, (_, _, english) in enumerate(batch)]
    references: dict[int, str] | None = None
    if ref_translations:
        references = {}
        for i, (_, h, _) in enumerate(batch, 1):
            ref = ref_translations.get(h, '')
            if ref.strip():
                references[i] = ref

    try:
        translations = translate_batch(api_url, numbered_items, lang, model=model, references=references)
    except Exception as e:
        return [(h, None, f'batch error: {e}') for _, h, _ in batch]

    results = []
    failed_items = []
    for seq_num, (_, h, english) in enumerate(batch, 1):
        if seq_num in translations and translations[seq_num].strip():
            results.append((h, translations[seq_num], None))
        else:
            failed_items.append((h, english))

    for h, english in failed_items:
        ref = ref_translations.get(h, '') if ref_translations else None
        try:
            translation = translate_single(api_url, english, lang, model=model, reference=ref or None)
            if translation.strip():
                results.append((h, translation, None))
            else:
                results.append((h, None, 'empty response'))
        except Exception as e:
            results.append((h, None, str(e)))

    return results


def translate_one(args: tuple[int, str, str, str, str, str | None, str | None]) -> tuple[int, str, str | None, str | None]:
    """Translate a single string (no-batch mode). Returns (seq, hash, translation, error)."""
    seq, h, english, api_url, lang, model, reference = args
    try:
        translation = translate_single(api_url, english, lang, model=model, reference=reference)
        if not translation.strip():
            return seq, h, None, 'empty response'
        return seq, h, translation, None
    except Exception as e:
        return seq, h, None, str(e)


def auto_batch_size(items: list[tuple[int, str, str]]) -> int:
    """Pick a batch size based on average string length."""
    if not items:
        return 1
    avg_tokens = sum(estimate_tokens(en) for _, _, en in items) / len(items)
    target = int(INPUT_TOKEN_BUDGET * 0.8 / max(avg_tokens + 10, 1))
    return max(1, min(target, 200))


def read_en_csv() -> list[tuple[str, str]]:
    """Read en.csv and return [(sha256, english_text), ...]."""
    en_file = TRANSLATIONS_DIR / 'en.csv'
    if not en_file.exists():
        return []
    with en_file.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        return [(row['sha256'], row['text']) for row in reader if row.get('sha256') and row.get('text')]


def read_lang_csv(lang: str) -> dict[str, str]:
    """Read a language CSV and return {sha256: translation}."""
    lang_file = TRANSLATIONS_DIR / f'{lang}.csv'
    if not lang_file.exists():
        return {}
    with lang_file.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        return {row['sha256']: row.get('text', '') for row in reader if row.get('sha256')}


def save_lang_csv(lang: str, translations: dict[str, str], en_entries: list[tuple[str, str]]) -> None:
    """Write a language CSV sorted by sha256."""
    lang_file = TRANSLATIONS_DIR / f'{lang}.csv'
    with lang_file.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['sha256', 'text'], quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for h, _ in sorted(en_entries, key=lambda r: r[0]):
            writer.writerow({'sha256': h, 'text': translations.get(h, '')})


def main() -> None:
    parser = argparse.ArgumentParser(description='Translate missing strings using LM Studio.')
    parser.add_argument('--api-url', default=DEFAULT_API_URL, help=f'LM Studio API URL (default: {DEFAULT_API_URL})')
    parser.add_argument('--language', default='zh-CN', help='Target language code (default: zh-CN)')
    parser.add_argument('--model', default=None, help='Model name to use (e.g. gemma-3-4b)')
    parser.add_argument('--workers', type=int, default=2, help='Concurrent translation requests (default: 2)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be translated without calling API')
    parser.add_argument('--start-from', type=int, default=0, help='Skip first N missing strings (for resuming)')
    parser.add_argument('--limit', type=int, default=0, help='Translate at most N strings (0 = all)')
    parser.add_argument('--batch-size', type=int, default=0,
                        help='Strings per API call (0 = auto, based on avg length)')
    parser.add_argument('--no-batch', action='store_true', help='Disable batching (one string per API call)')
    parser.add_argument('--reference-language', default=None,
                        help='Reference language for context (e.g. zh-CN)')
    args = parser.parse_args()

    target_lang = args.language

    # Read English entries
    en_entries = read_en_csv()
    if not en_entries:
        print(f'Error: {TRANSLATIONS_DIR / "en.csv"} not found or empty. Run i18n_bootstrap.py first.')
        sys.exit(1)

    # Build hash -> english mapping
    hash_to_english: dict[str, str] = {h: en for h, en in en_entries}

    # Load reference translations if requested
    ref_translations: dict[str, str] | None = None
    if args.reference_language:
        ref_translations = read_lang_csv(args.reference_language)
        ref_count = sum(1 for v in ref_translations.values() if v.strip())
        print(f'Loaded {ref_count} reference translations from {args.reference_language}')

    # Read existing translations for target language
    existing = read_lang_csv(target_lang)

    # Find missing translations
    missing_hashes = [h for h, _ in en_entries if not existing.get(h, '').strip()]
    total_missing = len(missing_hashes)
    print(f'Found {total_missing}/{len(en_entries)} missing {target_lang} translations')

    if args.start_from > 0:
        missing_hashes = missing_hashes[args.start_from:]
        print(f'Skipping first {args.start_from}, {len(missing_hashes)} remaining')

    if args.limit > 0:
        missing_hashes = missing_hashes[:args.limit]
        print(f'Limiting to {len(missing_hashes)} strings')

    if not missing_hashes:
        print('Nothing to translate!')
        return

    # Build work items: (seq, hash, english)
    items = [(seq, h, hash_to_english[h]) for seq, h in enumerate(missing_hashes)]

    if args.dry_run:
        batch_size = 1 if args.no_batch else (args.batch_size or auto_batch_size(items))
        mode = 'single-string' if args.no_batch else f'batch (size ~{batch_size})'
        print(f'\nDry run: would translate {len(items)} strings to {target_lang}, mode={mode}, workers={args.workers}')
        if args.model:
            print(f'  Model: {args.model}')
        for _, h, english in items[:5]:
            preview = english[:80].replace('\n', '\\n')
            print(f'  [{h[:12]}...] {preview}...')
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

    def save_progress() -> None:
        save_lang_csv(target_lang, existing, en_entries)

    translated_count = 0
    failed_count = 0
    total = len(items)
    t_start = time.time()
    last_save_time = t_start

    def maybe_save() -> None:
        nonlocal last_save_time
        now = time.time()
        if now - last_save_time >= SAVE_INTERVAL:
            print(f'  -- Saving progress ({translated_count} done) --')
            save_progress()
            last_save_time = now

    if args.no_batch:
        print(f'\nTranslating {total} strings to {target_lang} one-at-a-time with {args.workers} workers...\n')
        work = [
            (seq, h, english, args.api_url, target_lang, args.model,
             (ref_translations.get(h) or None) if ref_translations else None)
            for seq, h, english in items
        ]
        try:
            with ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = {executor.submit(translate_one, w): w for w in work}
                for future in as_completed(futures):
                    _, h, translation, error = future.result()
                    en_preview = hash_to_english[h][:60].replace('\n', '\\n')
                    if translation:
                        existing[h] = translation
                        translated_count += 1
                        tr_preview = translation[:60].replace('\n', '\\n')
                        elapsed = time.time() - t_start
                        rate = translated_count / elapsed * 60 if elapsed > 0 else 0
                        print(f'  [{translated_count}/{total}] ({rate:.0f}/min) "{en_preview}..."')
                        print(f'    -> "{tr_preview}..."')
                    else:
                        failed_count += 1
                        print(f'  FAILED [{failed_count}] "{en_preview}...": {error}')
                    maybe_save()
        except KeyboardInterrupt:
            print('\n\nInterrupted! Saving progress...')
    else:
        batch_size = args.batch_size or auto_batch_size(items)
        batches = create_batches(items, batch_size)
        print(f'\nTranslating {total} strings to {target_lang} in {len(batches)} batches '
              f'(~{batch_size} strings/batch) with {args.workers} workers...\n')

        try:
            with ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = {
                    executor.submit(process_batch, batch, args.api_url, target_lang, args.model,
                                    ref_translations): batch
                    for batch in batches
                }
                for future in as_completed(futures):
                    results = future.result()
                    for h, translation, error in results:
                        en_preview = hash_to_english[h][:60].replace('\n', '\\n')
                        if translation:
                            existing[h] = translation
                            translated_count += 1
                            tr_preview = translation[:60].replace('\n', '\\n')
                            elapsed = time.time() - t_start
                            rate = translated_count / elapsed * 60 if elapsed > 0 else 0
                            print(f'  [{translated_count}/{total}] ({rate:.0f}/min) "{en_preview}..."')
                            print(f'    -> "{tr_preview}..."')
                        else:
                            failed_count += 1
                            print(f'  FAILED [{failed_count}] "{en_preview}...": {error}')
                    maybe_save()
        except KeyboardInterrupt:
            print('\n\nInterrupted! Saving progress...')

    # Final save
    print(f'\nSaving final results to {TRANSLATIONS_DIR / f"{target_lang}.csv"}...')
    save_progress()

    elapsed = time.time() - t_start
    still_missing = sum(1 for h, _ in en_entries if not existing.get(h, '').strip())
    print(f'\nDone in {elapsed:.0f}s! Translated: {translated_count}, Failed: {failed_count}')
    print(f'Still missing: {still_missing}/{len(en_entries)}')


if __name__ == '__main__':
    main()
