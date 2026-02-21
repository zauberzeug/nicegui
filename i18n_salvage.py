#!/usr/bin/env python3
"""Salvage Chinese translations from https://github.com/Yuerchu/NiceGUI-docs.

Parses the Chinese VitePress documentation files and matches their content
to English strings in the per-language CSVs using structural mapping (doc file names
-> registry page names -> part titles -> descriptions).

Each language is stored in a separate CSV file linked by SHA-256 hash of the English text.

Usage:
    python i18n_salvage.py                    # apply salvaged translations
    python i18n_salvage.py --dry-run          # preview matches without writing
    python i18n_salvage.py --repo /path/to    # custom repo path
"""
import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path

TRANSLATIONS_DIR = Path(__file__).parent / 'website' / 'translations'
DEFAULT_REPO = Path('/tmp/NiceGUI-docs/docs')
TARGET_LANG = 'zh-CN'

# Map Chinese doc filenames -> NiceGUI registry page names
ELEMENT_FILE_TO_REGISTRY = {
    'badge': 'badge',
    'button': 'button',
    'button_dropdown': 'button_dropdown',
    'button_group': 'button_group',
    'chat_message': 'chat_message',
    'checkbox': 'checkbox',
    'chip': 'chip',
    'codemirror': 'codemirror',
    'color_input': 'color_input',
    'color_picker': 'color_picker',
    'date': 'date',
    'element': 'element',
    'fab': 'fab',
    'html': 'html',
    'input': 'input',
    'input_chips': 'input_chips',
    'joystick': 'joystick',
    'knob': 'knob',
    'label': 'label',
    'link': 'link',
    'markdown': 'markdown',
    'mermaid': 'mermaid',
    'number': 'number',
    'radio': 'radio',
    'range': 'range',
    'rating': 'rating',
    'restructured_text': 'restructured_text',
    'select': 'select',
    'slider': 'slider',
    'switch': 'switch',
    'textarea': 'textarea',
    'time': 'time',
    'toggle': 'toggle',
    'upload': 'upload',
}

# Map section filenames -> registry page names
SECTION_FILE_TO_REGISTRY = {
    'section_text_elements': 'section_text_elements',
    'section_controls': 'section_controls',
    'section_audiovisual_elements': 'section_audiovisual_elements',
    'section_data_elements': 'section_data_elements',
    'section_binding_properties': 'section_binding_properties',
    'section_page_layout': 'section_page_layout',
    'section_styling_appearance': 'section_styling_appearance',
    'section_action_events': 'section_action_events',
    'section_pages_routing': 'section_pages_routing',
    'section_configuration_deployment': 'section_configuration_deployment',
    'section_testing': 'section_testing',
}

# Known heading -> English part title mappings (Chinese heading -> English title)
HEADING_TO_TITLE: dict[str, str] = {
    # Button demos
    '图标': 'Icons',
    '等待按钮点击': 'Await button click',
    '使用上下文管理器禁用按钮': 'Disable button with a context manager',
    '自定义切换按钮': 'Custom toggle button',
    '浮动操作按钮': 'Floating Action Button',
    '可展开的浮动操作按钮': 'Expandable Floating Action Button',
    # Badge demos
    '角标定位': 'Badge Placement',
    # Button group demos
    '按钮组样式': 'Button group styling',
    '下拉按钮组合按钮组': 'Button group with dropdown button',
    # Checkbox demos
    '处理用户交互': 'Handle User Interaction',
    # Chip demos
    '芯片外观': 'Chip Appearance',
    '动态芯片元素（标签/标记）': 'Dynamic chip elements as labels/tags',  # noqa: RUF001
    # CodeMirror demos
    '代码编辑器主题': 'Theme',
    '代码编辑器语言支持': 'Supported Languages',
    # Color input
    '自定义颜色选择器': 'Customize the Color Picker',
    # Date
    '日期输入和日期选择器': 'Input element with date picker',
    '日期范围输入': 'Date range input',
    '日期过滤器': 'Date filter',
    # Input
    '自动补全': 'Autocompletion',
    '可清除': 'Clearable',
    '样式设置': 'Styling',
    '输入验证': 'Input validation',
    '延迟验证': 'Lazy validation',
    '客户端验证': 'Client-side validation',
    # Input chips
    '自动分割值': 'Auto-split values',
    # Joystick
    '虚拟摇杆': 'Joystick',
    # Knob
    '旋钮': 'Knob',
    # Label
    '根据内容改变外观': 'Change Appearance Depending on the Content',
    # Link
    '大型页面导航': 'Navigate on large pages',
    '链接到其他页面': 'Links to other pages',
    '从图片和其他元素中创建链接': 'Link from images and other elements',
    # Markdown
    '带缩进的 Markdown': 'Markdown with indentation',
    '带代码块的 Markdown': 'Markdown with code blocks',
    'Markdown 表格': 'Markdown tables',
    'Mermaid 图表': 'Mermaid diagrams',
    'LaTeX 公式': 'LaTeX formulas',
    '更改 Markdown 内容': 'Change Markdown content',
    # Number
    '自定义格式化': 'Custom sorting and formatting',
    # Radio
    '注入任意内容': 'Inject arbitrary content',
    # Range
    '范围选择器': 'Range',
    # Rating
    '自定义图标': 'Customize icons',
    '自定义颜色': 'Customize color',
    '自定义标签': 'Customize labels',
    # Select
    '输入即搜索': 'Search-as-you-type',
    '多选': 'Multi selection',
    '更新选项': 'Update options',
    # Slider
    '禁用滑块': 'Disable slider',
    # Switch
    '开关': 'Switch',
    # Textarea
    '多行文本输入': 'Textarea',
    # Upload
    '上传事件参数': 'Upload event arguments',
    '上传限制': 'Upload restrictions',
    '显示文件内容': 'Show file content',
    '上传大文件': 'Uploading large files',
    # Chat message
    '带有子元素的聊天消息': 'Chat message with child elements',
    # Generic Element
    '通用 Element': 'Generic Element',
    # HTML
    '内联元素': 'Producing in-line elements',
    '其他 HTML 元素': 'Other HTML Elements',
    # ReStructuredText
    '重构文本': 'ReStructuredText',

    # Overview page
    '概览': 'Overview',
    '如何使用本指南': 'How to use this guide',
    '基本概念': 'Basic concepts',
    '动作、事件与任务': 'Actions, Events and Tasks',
    '实现原理': 'Implementation',
    '运行 NiceGUI 应用': 'Running NiceGUI Apps',
    '自定义扩展': 'Customization',
    '测试框架': 'Testing',

    # Section titles
    '控制元素': 'Controls',
    '文本元素': 'Text Elements',
    '视听元素': 'Audiovisual Elements',
    '数据元素': 'Data Elements',
    '绑定属性': 'Binding Properties',
    '页面布局': 'Page Layout',
    '样式与外观': 'Styling & Appearance',
    '动作与事件': 'Action & Events',
    '页面与路由': 'Pages & Routing',
    '配置与部署': 'Configuration & Deployment',
    '测试': 'Testing',
}


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def parse_markdown_sections(content: str) -> list[tuple[str, str, int]]:
    """Parse markdown into (heading, body_text, heading_level) tuples."""
    sections: list[tuple[str, str, int]] = []
    lines = content.split('\n')
    current_heading = ''
    current_level = 0
    current_body: list[str] = []

    for line in lines:
        heading_match = re.match(r'^(#{1,4})\s+(.+)$', line)
        if heading_match:
            if current_heading:
                body = '\n'.join(current_body).strip()
                sections.append((current_heading, body, current_level))
            current_level = len(heading_match.group(1))
            current_heading = heading_match.group(2).strip()
            current_body = []
        else:
            current_body.append(line)

    if current_heading:
        body = '\n'.join(current_body).strip()
        sections.append((current_heading, body, current_level))

    return sections


def clean_heading(heading: str) -> str:
    """Remove backtick code, badges, and extra formatting from headings."""
    heading = re.sub(r'\s*`[^`]+`', '', heading)
    heading = re.sub(r'\s*<Badge[^>]*>', '', heading)
    return heading.strip()


def extract_description_from_body(body: str) -> str:
    """Extract the description paragraph from a section body."""
    lines = body.split('\n')
    paragraphs: list[str] = []
    current: list[str] = []
    in_code_block = False
    in_directive = False

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            if current:
                paragraphs.append('\n'.join(current))
                current = []
            continue
        if in_code_block:
            continue
        if line.strip().startswith(':::'):
            in_directive = not in_directive
            continue
        if in_directive:
            continue
        if line.strip().startswith('<!--@include:'):
            continue
        if line.strip().startswith('|') or line.strip().startswith('[查看更多'):
            continue
        if not line.strip():
            if current:
                paragraphs.append('\n'.join(current))
                current = []
            continue
        current.append(line)

    if current:
        paragraphs.append('\n'.join(current))

    for p in paragraphs:
        text = p.strip()
        if len(text) > 5 and not text.startswith('[') and not text.startswith('<!--'):
            return text

    return ''


def read_en_csv() -> list[tuple[str, str]]:
    """Read en.csv and return [(sha256, english_text), ...]."""
    en_file = TRANSLATIONS_DIR / 'en.csv'
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


def build_en_index(en_entries: list[tuple[str, str]]) -> dict[str, str]:
    """Build {english_string: sha256} mapping."""
    index: dict[str, str] = {}
    for h, en in en_entries:
        if en not in index:
            index[en] = h
    return index


def normalize_whitespace(s: str) -> str:
    """Normalize whitespace for comparison."""
    return ' '.join(s.split())


def find_best_match(english: str, en_index: dict[str, str]) -> str | None:
    """Find the best matching hash for an English string."""
    if english in en_index:
        return en_index[english]
    normalized = normalize_whitespace(english)
    for en, h in en_index.items():
        if normalize_whitespace(en) == normalized:
            return h
    return None


def process_element_file(filepath: Path, registry_name: str,
                         en_index: dict[str, str], existing: dict[str, str],
                         registry: dict) -> list[tuple[str, str]]:
    """Process a Chinese element doc file and return (sha256, chinese) pairs."""
    content = filepath.read_text(encoding='utf-8')
    sections = parse_markdown_sections(content)
    matches: list[tuple[str, str]] = []

    if registry_name not in registry:
        return matches

    page = registry[registry_name]

    for heading, body, _level in sections:
        clean = clean_heading(heading)
        english_title = HEADING_TO_TITLE.get(clean)

        desc = extract_description_from_body(body)
        if not desc:
            continue

        if english_title:
            for part in page.parts:
                if part.title == english_title and part.description:
                    en_desc = part.description.strip()
                    h = en_index.get(en_desc)
                    if h:
                        matches.append((h, desc))
                    break

    # Also try matching the main element description (first part)
    if page.parts and page.parts[0].description:
        main_desc_en = page.parts[0].description.strip()
        h = en_index.get(main_desc_en)
        if h and not existing.get(h, '').strip():
            for _heading, body, level in sections:
                if level == 1:
                    desc = extract_description_from_body(body)
                    if desc:
                        matches.append((h, desc))
                    break

    return matches


def process_overview(filepath: Path, en_index: dict[str, str],
                     registry: dict) -> list[tuple[str, str]]:
    """Process the documentation overview/index page."""
    content = filepath.read_text(encoding='utf-8')
    sections = parse_markdown_sections(content)
    matches: list[tuple[str, str]] = []

    if '' not in registry:
        return matches

    page = registry['']

    for heading, body, _level in sections:
        clean = clean_heading(heading)
        english_title = HEADING_TO_TITLE.get(clean)
        if not english_title:
            continue

        desc = extract_description_from_body(body)
        if not desc:
            continue

        for part in page.parts:
            if part.title == english_title and part.description:
                en_desc = part.description.strip()
                h = en_index.get(en_desc)
                if h:
                    matches.append((h, desc))
                break

    return matches


def salvage_short_strings(en_index: dict[str, str]) -> list[tuple[str, str]]:
    """Provide translations for short well-known strings."""
    known: dict[str, str] = {
        '*Controls*': '*控制元素*',
        'Controls': '控制元素',
        '*Text* Elements': '*文本*元素',
        'Text Elements': '文本元素',
        '*Audiovisual* Elements': '*视听*元素',
        'Audiovisual Elements': '视听元素',
        '*Data* Elements': '*数据*元素',
        'Data Elements': '数据元素',
        '*Binding* Properties': '*绑定*属性',
        'Binding Properties': '绑定属性',
        '*Pages* & Routing': '*页面*与路由',
        '*Testing*': '*测试*',
        'Action & *Events*': '动作与*事件*',
        'Action & Events': '动作与事件',
        '*NiceGUI* Documentation': '*NiceGUI* 文档',
        'Configuration & Deployment': '配置与部署',
        'Documentation': '文档',
        'Examples': '示例',
        'Demos': '演示',
        'Overview': '概览',
        'Basic concepts': '基本概念',
        'How to use this guide': '如何使用本指南',
        'Actions, Events and Tasks': '动作、事件与任务',
        'Implementation': '实现原理',
        'Running NiceGUI Apps': '运行 NiceGUI 应用',
        'Customization': '自定义扩展',
        'Testing': '测试',
        'Reference, Demos and more': '参考、演示和更多',
        'Search documentation': '搜索文档',
        'Button': '按钮',
        'Button Group': '按钮组',
        'Dropdown Button': '下拉按钮',
        'Badge': '角标',
        'Chip': '芯片',
        'Toggle': '切换器',
        'Checkbox': '复选框',
        'Switch': '开关',
        'Slider': '滑块',
        'Knob': '旋钮',
        'Joystick': '虚拟摇杆',
        'Label': '标签',
        'Link': '链接',
        'Chat Message': '聊天消息',
        'Markdown': 'Markdown',
        'Mermaid Diagrams': 'Mermaid 图表',
        'HTML': 'HTML',
        'Image': '图片',
        'Audio': '音频',
        'Video': '视频',
        'Icon': '图标',
        'Avatar': '头像',
        'SVG': 'SVG',
        'Table': '表格',
        'AG Grid': 'AG Grid',
        'Highcharts': 'Highcharts',
        'Apache EChart': 'Apache EChart',
        'Pyplot': 'Pyplot',
        'Matplotlib': 'Matplotlib',
        'Plotly': 'Plotly',
        'Circular Progress': '环形进度条',
        'Linear Progress': '线性进度条',
        'Spinner': '加载动画',
        '3D Scene': '3D 场景',
        'Tree': '树形控件',
        'Log': '日志视图',
        'Editor': '编辑器',
        'Code': '代码',
        'JSON Editor': 'JSON 编辑器',
        'Card': '卡片',
        'Column Element': '列元素',
        'Row Element': '行元素',
        'Grid Element': '网格元素',
        'Expansion Element': '折叠面板',
        'Scroll Area': '滚动区域',
        'Separator': '分隔符',
        'Splitter': '分割面板',
        'Tabs': '标签页',
        'Stepper': '步骤条',
        'Timeline': '时间线',
        'Carousel': '轮播图',
        'Pagination': '分页',
        'Menu': '菜单',
        'Context Menu': '右键菜单',
        'Tooltip': '工具提示',
        'Notification': '通知',
        'Dialog': '对话框',
        'Color Theming': '颜色主题',
        'Dark mode': '深色模式',
        'Dropdown Selection': '下拉选择器',
        'Date Picker': '日期选择器',
        'Date Input': '日期输入',
        'Time Input': '时间输入',
        'Color Input': '颜色输入',
        'Color Picker': '颜色选择器',
        'Number Input': '数字输入',
        'CodeMirror': 'CodeMirror',
        'Textarea': '多行文本输入',
        'Icons': '图标',
        'Await button click': '等待按钮点击',
        'Disable button with a context manager': '使用上下文管理器禁用按钮',
        'Custom toggle button': '自定义切换按钮',
        'Floating Action Button': '浮动操作按钮',
        'Expandable Floating Action Button': '可展开的浮动操作按钮',
        'Autocompletion': '自动补全',
        'Clearable': '可清除',
        'Styling': '样式设置',
        'Input validation': '输入验证',
        'Lazy validation': '延迟验证',
        'Client-side validation': '客户端验证',
        'Search-as-you-type': '输入即搜索',
        'Multi selection': '多选',
        'Update options': '更新选项',
        'Handle User Interaction': '处理用户交互',
        'Inject arbitrary content': '注入任意内容',
        'Auto-split values': '自动分割值',
        'Disable slider': '禁用滑块',
        'Upload event arguments': '上传事件参数',
        'Upload restrictions': '上传限制',
        'Show file content': '显示文件内容',
        'Uploading large files': '上传大文件',
        'Navigate on large pages': '大型页面导航',
        'Links to other pages': '链接到其他页面',
        'Link from images and other elements': '从图片和其他元素中创建链接',
        'Markdown with indentation': '带缩进的 Markdown',
        'Markdown with code blocks': '带代码块的 Markdown',
        'Markdown tables': 'Markdown 表格',
        'Mermaid diagrams': 'Mermaid 图表',
        'LaTeX formulas': 'LaTeX 公式',
        'Change Markdown content': '更改 Markdown 内容',
        'Change Appearance Depending on the Content': '根据内容改变外观',
        'Date filter': '日期过滤器',
        'Date range input': '日期范围输入',
        'Customize the Color Picker': '自定义颜色选择器',
        'Customize icons': '自定义图标',
        'Customize color': '自定义颜色',
        'Customize labels': '自定义标签',
        'Producing in-line elements': '内联元素',
        'Other HTML Elements': '其他 HTML 元素',
        'Chat message with child elements': '带有子元素的聊天消息',
        'Input element with date picker': '日期输入和日期选择器',
        'Button group styling': '按钮组样式',
        'Button group with dropdown button': '下拉按钮组合按钮组',
        'Badge Placement': '角标定位',
        'Chip Appearance': '芯片外观',
        'Dynamic chip elements as labels/tags': '动态芯片元素（标签/标记）',  # noqa: RUF001
        'Page Layout': '页面布局',
        'Clear Containers': '清除容器',
        'Teleport': '传送',
        'Styling & *Appearance*': '样式与*外观*',
        'Styling & Appearance': '样式与外观',
        'CSS Variables': 'CSS 变量',
        'CSS Layers': 'CSS 层',
        'Default classes': '默认类',
        'Default props': '默认属性',
        'Default style': '默认样式',
        'Timer': '定时器',
        'Keyboard': '键盘',
        'Events': '事件',
        'Background Tasks': '后台任务',
        'Bindings': '绑定',
        'Error handling': '错误处理',
        'Auto-index page': '自动索引页面',
        'Native Mode': '窗口模式',
        'Environment Variables': '环境变量',
        'Custom Vue Components': '自定义 Vue 组件',
        'Server Hosting': '服务器托管',
        'Enjoy!': '使用愉快！',  # noqa: RUF001
        '...and many more': '……还有更多',
        'Become a sponsor': '成为赞助者',
        'Browse through plenty of live demos.': '浏览大量的在线演示。',
        'Browse through plenty of examples.': '浏览大量的示例。',
        'Interaction': '交互',
        'Layout': '布局',
        'Visualization': '可视化',
        'Code *nicely*': '*优雅*编程',
        'Coding': '编程',
        'Imprint': '版权声明',
        'Privacy': '隐私政策',
        'Privacy Policy': '隐私政策',
        'Additional Resources': '附加资源',
        'Captions and Overlays': '标题和叠加层',
        'Interactive Image': '交互式图片',
        'Bind to dictionary': '绑定到字典',
        'Bind to storage': '绑定到存储',
        'Bind to variable': '绑定到变量',
        'Bindable dataclass': '可绑定数据类',
        'Bindable properties for maximum performance': '可绑定属性以获得最佳性能',
        'Binding to a switch': '绑定到开关',
        'Download file from local path': '从本地路径下载文件',
        'Download from a relative URL': '从相对 URL 下载',
        'Download functions': '下载函数',
        'Download raw bytes or string content': '下载原始字节或字符串内容',
        '3D Graphing': '3D 图表',
        'Scene View': '场景视图',
        'Draggable objects': '可拖拽对象',
        'Camera Parameters': '相机参数',
        'Custom Composed 3D Objects': '自定义组合 3D 对象',
        'Blank canvas': '空白画布',
        'Leaflet Map': 'Leaflet 地图',
        'Add Markers on Click': '点击添加标记',
        'Adding layers': '添加图层',
        'Changing the Map Style': '更改地图样式',
        'Draw on Map': '在地图上绘制',
        'Draw with Custom Options': '使用自定义选项绘制',
        'Disable Pan and Zoom': '禁用平移和缩放',
        'Adding rows': '添加行',
        'Adding Sub Pages': '添加子页面',
        'Async Sub Pages': '异步子页面',
        'Async event handlers': '异步事件处理器',
        'Async execution': '异步执行',
        'Custom Background': '自定义背景',
        'Custom Grid': '自定义网格',
        'Custom colors': '自定义颜色',
        'Custom error page': '自定义错误页面',
        'Custom events': '自定义事件',
        'Custom welcome message': '自定义欢迎消息',
        'Dark Reader extension': '深色阅读器扩展',
        'Disable Dark Reader extension': '禁用深色阅读器扩展',
        'Dictionary interface': '字典接口',
        'Dynamic Stepper': '动态步骤条',
        'ElementFilter': 'ElementFilter',
        'Event': '事件',
        'Event subscription': '事件订阅',
        'Computed fields': '计算字段',
        'Computed props': '计算属性',
        'Conditional formatting': '条件格式',
        'Configuration': '配置',
        'Component Selection': '组件选择',
        'Crosshairs': '十字准线',
        'Advanced usage': '高级用法',
        'Emoji favicon': 'Emoji 图标',
        'Base64 favicon': 'Base64 图标',
        'Fullscreen': '全屏',
        'Safe Input Parsing': '安全输入解析',
        'Script Mode': '脚本模式',
        'Space': '占位空间',
        'Skeleton': '骨架屏',
        'auto-reload on code change': '代码修改时自动重载',
        'Awaitable dialog': '可等待的对话框',
        'Awaitable refresh': '可等待的刷新',
        'Cancel current invocation': '取消当前调用',
        'Card without shadow': '无阴影卡片',
        'Context menus with dynamic content': '动态内容的右键菜单',
        'Context menu for 3D objects': '3D 对象的右键菜单',
        'Control the audio element': '控制音频元素',
        'Control the video element': '控制视频元素',
        'Counting page visits': '统计页面访问量',
        'Custom grid layout': '自定义网格布局',
        'If you like NiceGUI, go and become a': '如果您喜欢 NiceGUI，请成为一位',  # noqa: RUF001
        'Map of NiceGUI': 'NiceGUI 概览图',
    }

    matches: list[tuple[str, str]] = []
    for en, zh in known.items():
        h = en_index.get(en)
        if h:
            matches.append((h, zh))

    return matches


def main() -> None:
    parser = argparse.ArgumentParser(description='Salvage Chinese translations from NiceGUI-docs repo.')
    parser.add_argument('--repo', type=Path, default=DEFAULT_REPO, help='Path to NiceGUI-docs/docs/')
    parser.add_argument('--dry-run', action='store_true', help='Preview matches without writing CSV')
    args = parser.parse_args()

    if not args.repo.exists():
        print(f'Error: {args.repo} not found. Clone it first:')
        print('  git clone --depth 1 https://github.com/Yuerchu/NiceGUI-docs.git /tmp/NiceGUI-docs')
        sys.exit(1)

    en_entries = read_en_csv()
    if not en_entries:
        print(f'Error: {TRANSLATIONS_DIR / "en.csv"} not found or empty. Run i18n_bootstrap.py first.')
        sys.exit(1)

    en_index = build_en_index(en_entries)
    existing = read_lang_csv(TARGET_LANG)

    # Load registry for structural matching
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from website.documentation.content.doc.api import registry
    except Exception as e:
        print(f'Warning: could not import registry: {e}')
        registry = {}

    all_matches: list[tuple[str, str]] = []

    # 1. Salvage short/known strings
    short_matches = salvage_short_strings(en_index)
    all_matches.extend(short_matches)
    print(f'Known short strings: {len(short_matches)} matches')

    # 2. Process element doc files
    elements_dir = args.repo / 'documentation' / 'elements'
    if elements_dir.exists():
        for md_file in sorted(elements_dir.glob('*.md')):
            stem = md_file.stem
            if stem in ELEMENT_FILE_TO_REGISTRY:
                reg_name = ELEMENT_FILE_TO_REGISTRY[stem]
                matches = process_element_file(md_file, reg_name, en_index, existing, registry)
                if matches:
                    all_matches.extend(matches)
                    print(f'  {stem}.md: {len(matches)} matches')

    # 3. Process overview/index
    doc_index = args.repo / 'documentation' / 'index.md'
    if doc_index.exists():
        matches = process_overview(doc_index, en_index, registry)
        if matches:
            all_matches.extend(matches)
            print(f'  documentation/index.md: {len(matches)} matches')

    # Apply matches
    applied = 0
    skipped = 0
    hash_to_english = {h: en for h, en in en_entries}
    for h, chinese in all_matches:
        if existing.get(h, '').strip():
            skipped += 1
            continue
        existing[h] = chinese
        applied += 1
        if args.dry_run:
            en_text = hash_to_english.get(h, '?')
            en_preview = en_text[:60].replace('\n', '\\n')
            zh_preview = chinese[:60].replace('\n', '\\n')
            print(f'  MATCH: "{en_preview}..."')
            print(f'      -> "{zh_preview}..."')

    print(f'\nTotal: {len(all_matches)} matches, {applied} applied, {skipped} already translated')

    if not args.dry_run:
        # Write back
        lang_file = TRANSLATIONS_DIR / f'{TARGET_LANG}.csv'
        with lang_file.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['sha256', 'text'])
            writer.writeheader()
            for h, _ in en_entries:
                writer.writerow({'sha256': h, 'text': existing.get(h, '')})
        print(f'Saved to {lang_file}')

    still_missing = sum(1 for h, _ in en_entries if not existing.get(h, '').strip())
    print(f'Still missing: {still_missing}/{len(en_entries)}')


if __name__ == '__main__':
    main()
