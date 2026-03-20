# Website Development Guidelines

## Styling

- **Tailwind over `.style()`**: Use Tailwind arbitrary values (e.g. `text-[#5898d4]`, `bg-[rgba(0,0,0,0.06)]`) instead of `.style()`. Only use `.style()` for things Tailwind can't express (nested selectors, `box-shadow` with `color-mix`, non-standard border widths like `1.5px`).
- **Inline classes**: Keep `.classes()` calls on one line where feasible. Avoid splitting across multiple lines unless truly long.
- **Minimize custom CSS**: Before adding CSS to `style.css`, check if Tailwind can handle it. Use arbitrary variants like `[&_li]:text-sm` to style nested HTML elements.
- **Keep native browser behaviors**: Prefer native list bullets over custom `::before` pseudo-elements. Style them with Tailwind rather than replacing them.
- **Use `ui.grid()`** instead of `ui.element().classes('grid ...')`.
- **Use `ui.element()`** without arguments — `'div'` is the default.
- **Design constants**: Use constants from `design.py` (e.g. `d.BG_BLUE`, `d.TEXT_SECONDARY`, `d.BORDER`) in f-string `.classes()` calls. Raw color values live in `design.py`, not in components or CSS.

## Component Structure

- **`create()` first, helpers below**: Each section file has a public `create()` function at the top. Private helper functions (`_func`) go below it.
- **Use `section()` context manager** from `shared.py` for consistent section wrapping (padding, max-width, link targets). Exception: the hero section is too different and uses its own layout.
- **Use `section_heading()`** for consistent label + title + description groups.
- **Use existing window functions** from `documentation/windows.py` (`python_window`, `bash_window`, `browser_window`) — don't reimplement code/browser chrome.

## Theming

- **Dark mode** uses Quasar's `.body--dark` class, not Tailwind's `dark:`. Use `dark:` in Tailwind classes for dark-mode variants — Tailwind is configured to respect `.body--dark`.
- **`themed_image()`** from `utils.py` handles light/dark image variants. Pass a path with `THEME` placeholder (e.g., `logo.THEME.webp`).
- **Phosphor icons** via the shared helper instead of inline SVG or Material icons for decorative/brand icons.

## Interactivity

- **Python over JS**: Prefer Python handlers (`on_click=`, `ui.run_javascript()`, `ui.tooltip()`) over raw `js_handler` strings. JS is harder to debug and breaks more easily.
- **Scroll reveal**: Use the `reveal` class. For staggered animations, use Tailwind's `delay-250!` / `delay-500!` (the `!` makes it `!important`, which overrides the `transition` shorthand in CSS that resets delay).

## Layout

- **Grid for responsive layouts**: Use CSS grid (`ui.grid().classes('grid-cols-3 max-lg:grid-cols-1')`) instead of flex-wrap with breakpoints. Grid gives more predictable control over column sizing.
- **Quasar quirks**: Quasar sets its own `color: white` on `.q-header` and `background: #f8f8f8` on `<html>`. Override these explicitly when needed.
