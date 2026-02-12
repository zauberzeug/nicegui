from nicegui import ui

from . import doc

doc.title('Security Best Practices')


doc.text('Security Model', '''
    NiceGUI provides secure defaults and built-in protections, but **developers must write secure code**.

    While most can, not all UI components can safely handle untrusted input.
    Understanding which ones require validation is essential.

    **Framework provides:**

    - Secure defaults if possible,
    - Protection mechanisms,
    - Prompt vulnerability fixes

    **Developers must:**

    - Use Common Sense,
    - Keep sanitization enabled for untrusted content,
    - Validate user input if necessitated,
    - Install the latest NiceGUI version
''')


@doc.demo('Common Sense', '''
    At the end of the day, NiceGUI is Python.
    Do read through the application logic to see if it makes common sense.

    You may find that some security vulnerabilities are obvious and should never happen in production code.

    Here is a safe way to parse user input into Python data structures using `ast.literal_eval()`:
''')
def common_sense_demo():
    import ast

    def evaluate_safely():
        try:
            value = ast.literal_eval(user_input.value)
            ui.notify(f'Result: {value}')
        except (ValueError, SyntaxError):
            ui.notify('Invalid literal', type='negative')

    user_input = ui.input('Enter a Python literal', placeholder='[1, 2]')
    ui.button('Parse', on_click=evaluate_safely)


doc.text('', '''
    **Avoid at all costs:**
    ```python
    value = eval(user_input.value)  # Can execute ANY Python code!
    ```
''')


@doc.demo('Component Selection', '''
    Pick the most secure element to have NiceGUI work for you as much as possible.

    **Secure by default** (considering `sanitize=True` if applicable):

    - `ui.html()`,
    - `ui.markdown()`,
    - `ui.chat_message()`,
    - `ui.interactive_image()`
    - Any other element which serves a dedicated purpose, for which it is easy for NiceGUI to defend arbitrary user input.

    **You must validate, as the library can't distinguish the good and the bad**:

    - `ui.navigate.to()`,
    - `ui.link()`,
    - `element.style()`

    **Never with user input, unless you know what you are doing**:

    - `ui.add_head_html()`,
    - `ui.add_body_html()`,
    - `ui.add_css()`
''')
def component_security_overview_demo():
    username = ui.input('Enter your name')

    ui.label().bind_text_from(username, 'value')
    ui.markdown().bind_content_from(username, 'value')


doc.text('', '''
    **Avoid at all costs:**
    ```python
    ui.add_body_html(f"<div>Welcome {username}</div>")  # XSS: "<img src=x onerror=alert(1)>"
    ui.add_head_html(f"<script>alert('{username}')</script>")  # XSS: "');alert(1);//"
    ```
''')


@doc.demo('URL Validation', '''
    As `javascript:` URLs have their legitimate purpose in allowing a link to execute JavaScript
    without round-trip server involvement, NiceGUI does not validate URL schemes.

    You must validate user URLs to prevent `javascript:` URL injection.
''')
def url_validation_demo():
    from urllib.parse import urlparse

    def is_safe_url(url: str) -> bool:
        return urlparse(url.strip()).scheme in ('', 'http', 'https')

    def open_link(url: str) -> None:
        if is_safe_url(url):
            ui.navigate.to(url)
        else:
            ui.notify('Invalid or unsafe URL', type='negative')

    def show_link(url: str) -> None:
        if is_safe_url(url):
            ui.link(target=url)
        else:
            ui.notify('Invalid or unsafe URL', type='negative')

    user_url = ui.input('Enter URL', placeholder='javascript:alert(1)')
    ui.button('Navigate', on_click=lambda: open_link(user_url.value))
    ui.button('Show link', on_click=lambda: show_link(user_url.value))


doc.text('', '''
    **Avoid at all costs:**
    ```python
    ui.navigate.to(user_url.value)  # Allows javascript: URL injection!
    ui.link(user_url.value)  # Opens javascript: URLs without validation!
    ```
''')


@doc.demo('CSS Injection', '''
    As legitimate CSS, [CSS data exfiltration techniques](https://portswigger.net/research/blind-css-exfiltration)
    and malicious CSS cannot be distinguished by the library, element style properties are NOT escaped.

    Validate style values before applying user input:
''')
def css_injection_demo():
    import re

    def validate_color(color: str) -> bool:
        """Validate color is safe (hex or rgb format only)."""
        hex_pattern = r'^#[0-9a-fA-F]{3,6}$'
        rgb_pattern = r'^rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)$'
        return bool(re.match(hex_pattern, color) or re.match(rgb_pattern, color))

    user_color = ui.input('Enter color (e.g., #ff0000)', value='#0000ff')
    label = ui.label('Sample text')

    def apply_color():
        if validate_color(user_color.value):
            label.style['color'] = user_color.value
            ui.notify('Color applied', type='positive')
        else:
            ui.notify('Invalid color format', type='negative')

    ui.button('Apply Color', on_click=apply_color)


doc.text('', '''
    **Avoid at all costs:**
    ```python
    # Allows CSS injection and data exfiltration:
    label.style['color'] = user_color.value
    ```
''')


@doc.part('Additional Resources')
def additional_resources():
    ui.markdown('''
        ##### Security Advisories

        [NiceGUI Security Advisories](https://github.com/zauberzeug/nicegui/security/advisories) - Keep NiceGUI updated for latest fixes.

        ##### External Resources

        - [OWASP Top 10](https://owasp.org/www-project-top-ten/)
        - [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
        - [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
        - [DOMPurify](https://github.com/cure53/DOMPurify)

        ##### Key Principles

        1. Keep sanitization enabled (secure by default)
        2. Validate URLs (framework doesn't validate schemes)
        3. Validate CSS values (not escaped by framework)
        4. Only disable sanitization for trusted application content
        5. Use defense-in-depth (headers, CSP, validation)
        6. Keep NiceGUI updated

        **Remember: NiceGUI provides tools, developers must write secure code.**
    ''')
