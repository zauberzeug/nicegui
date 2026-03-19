"""Design constants for the NiceGUI website. Use via f-strings in .classes() calls."""

# --- Raw color values ---

BRAND_BLUE = '#5898d4'
BRAND_BLUE_LIGHT = '#7ab4e4'
WARM_ACCENT = '#f0a050'
WARM_GLOW = 'rgba(240,160,80,0.07)'

_BG_LIGHT = '#fafbfc'
_BG_DARK = '#0f1117'
_BG_SURFACE_LIGHT = '#ffffff'
_BG_SURFACE_DARK = '#181b23'
_BG_CODE_LIGHT = '#f0f4f8'
_BG_CODE_DARK = '#1e222c'
_BG_FOOTER_LIGHT = '#edf0f3'
_BG_FOOTER_DARK = f'color-mix(in_srgb,{_BG_DARK}_70%,black)'

_TEXT_PRIMARY_LIGHT = '#1a1d26'
_TEXT_PRIMARY_DARK = '#edeff3'
_TEXT_SECONDARY_LIGHT = '#5c6370'
_TEXT_SECONDARY_DARK = '#8b929e'
_TEXT_MUTED_LIGHT = '#9ca3af'
_TEXT_MUTED_DARK = '#565d6b'

_BORDER_LIGHT = 'rgba(0,0,0,0.06)'
_BORDER_DARK = 'rgba(255,255,255,0.08)'

# --- Tailwind class fragments ---

# Backgrounds
BG = f'bg-[{_BG_LIGHT}] dark:bg-[{_BG_DARK}]'
BG_SURFACE = f'bg-[{_BG_SURFACE_LIGHT}] dark:bg-[{_BG_SURFACE_DARK}]'
BG_CODE = f'bg-[{_BG_CODE_LIGHT}] dark:bg-[{_BG_CODE_DARK}]'
BG_FOOTER = f'bg-[{_BG_FOOTER_LIGHT}] dark:bg-[{_BG_FOOTER_DARK}]'
BG_BRAND_BLUE = f'bg-[{BRAND_BLUE}]'
BG_WARM_ACCENT = f'bg-[{WARM_ACCENT}]'
BG_SPONSORS = f'bg-[color-mix(in_srgb,{WARM_ACCENT}_3%,{_BG_LIGHT})] dark:bg-[color-mix(in_srgb,{WARM_ACCENT}_3%,{_BG_DARK})]'
BG_BORDER = f'bg-[{_BORDER_LIGHT}] dark:bg-[{_BORDER_DARK}]'

# Text
TEXT_PRIMARY = f'text-[{_TEXT_PRIMARY_LIGHT}] dark:text-[{_TEXT_PRIMARY_DARK}]'
TEXT_PRIMARY_IMPORTANT = f'!text-[{_TEXT_PRIMARY_LIGHT}] dark:!text-[{_TEXT_PRIMARY_DARK}]'
TEXT_SECONDARY = f'text-[{_TEXT_SECONDARY_LIGHT}] dark:text-[{_TEXT_SECONDARY_DARK}]'
TEXT_MUTED = f'text-[{_TEXT_MUTED_LIGHT}] dark:text-[{_TEXT_MUTED_DARK}]'
TEXT_BRAND_BLUE = f'text-[{BRAND_BLUE}]'
TEXT_WARM_ACCENT = f'text-[{WARM_ACCENT}]'

# Borders
BORDER = f'border border-[{_BORDER_LIGHT}] dark:border-[{_BORDER_DARK}]'
BORDER_B = f'border-b border-b-[{_BORDER_LIGHT}] dark:border-b-[{_BORDER_DARK}]'
BORDER_T = f'border-t border-t-[{_BORDER_LIGHT}] dark:border-t-[{_BORDER_DARK}]'
BORDER_2 = f'border-2 border-[{_BORDER_LIGHT}] dark:border-[{_BORDER_DARK}]'
BORDER_BRAND_BLUE = f'border-[1.5px] border-[{BRAND_BLUE}]'
BORDER_WARM_ACCENT = f'border-[{WARM_ACCENT}]'
BORDER_SUBTLE = f'border-[1.5px] border-[{_BORDER_LIGHT}] dark:border-[{_BORDER_DARK}]'

# Shadows
SHADOW_BRAND = f'shadow-[0_2px_8px_color-mix(in_srgb,{BRAND_BLUE}_30%,transparent)]'
SHADOW_CARD = 'shadow-[0_4px_24px_rgba(0,0,0,0.08)]'

# Font sizes
TEXT_13PX = 'text-[0.8125rem]'
TEXT_13PX_MONO = 'text-[0.8rem] font-mono'  # section label (slightly smaller for mono)
TEXT_15PX = 'text-[0.9375rem]'
TEXT_19PX = 'text-[1.1875rem]'
TEXT_32PX = 'text-[2rem]'
TEXT_HERO = 'text-[clamp(2.5rem,5vw,4.5rem)]'
TEXT_SECTION_TITLE = 'text-[clamp(1.8rem,3vw,3rem)]'
TEXT_CTA_TITLE = 'text-[clamp(1.5rem,2.5vw,2.25rem)]'

# Hero glow gradient (written with spaces for readability, then replaced)
BG_HERO_GLOW = (
    f'bg-[radial-gradient(ellipse at 40% 45%, color-mix(in srgb, {BRAND_BLUE} 7%, transparent) 0%, transparent 55%),'
    f'radial-gradient(ellipse at 60% 55%, color-mix(in srgb, {BRAND_BLUE_LIGHT} 4%, transparent) 0%, transparent 50%),'
    f'radial-gradient(ellipse at 50% 50%, {WARM_GLOW} 0%, transparent 65%)]'
).replace(' ', '_')
