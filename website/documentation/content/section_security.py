from nicegui import ui

from . import doc

doc.title('Security Best Practices')


doc.text('Security Model', '''
    NiceGUI provides secure defaults and built-in protections, but **developers must write secure code**.
    Not all UI components can safely handle untrusted input,
    so understanding which ones require validation is essential.

    **The framework provides:**

    - Secure defaults where possible
    - Built-in protection mechanisms
    - Timely vulnerability fixes

    **Developers are responsible for:**

    - Reviewing application logic for unsafe patterns
    - Keeping sanitization enabled for untrusted content
    - Validating user input where necessary
    - Keeping NiceGUI up to date
''')


@doc.demo('Safe Input Parsing', '''
    NiceGUI applications are Python code, and many security issues stem from unsafe Python patterns.
    Reviewing your application logic can reveal vulnerabilities that should never reach production.

    For example, use `ast.literal_eval()` to safely parse user input into Python data structures:
''')
def safe_input_parsing_demo():
    import ast

    def evaluate_safely():
        try:
            value = ast.literal_eval(user_input.value)
            ui.notify(f'Result: {value}')
        except (ValueError, SyntaxError):
            ui.notify('Invalid Python literal', type='negative')

    user_input = ui.input('Enter Python literal', placeholder='[1, 2]')
    ui.button('Parse', on_click=evaluate_safely)


doc.text('', '''
    **Never do this:**
    ```python
    value = eval(user_input.value)  # Can execute arbitrary Python code!
    ```
''')


@doc.demo('Component Selection', '''
    Choosing the right component reduces the need for manual validation.

    **Secure by default** (with `sanitize=True`, which is the default where applicable):

    - `ui.html()`,
    - `ui.markdown()`,
    - `ui.chat_message()`,
    - `ui.interactive_image()`
    - Other elements with a well-defined purpose that the framework can protect automatically.

    **Require developer validation** (the framework cannot distinguish safe from unsafe values):

    - `ui.navigate.to()`,
    - `ui.link()`,
    - `element.style()`

    **Never use with untrusted input:**

    - `ui.add_head_html()`,
    - `ui.add_body_html()`,
    - `ui.add_css()`,
    - `ui.run_javascript()`
''')
def component_security_overview_demo():
    username = ui.input('Enter name')

    ui.label().bind_text_from(username, 'value')
    ui.markdown().bind_content_from(username, 'value')


doc.text('', '''
    **Never do this:**
    ```python
    ui.add_body_html(f"<div>Welcome {username}</div>")  # XSS: "<img src=x onerror=alert(1)>"
    ui.add_head_html(f"<script>alert('{username}')</script>")  # XSS: "');alert(1);//"
    ```
''')


@doc.demo('URL Validation', '''
    NiceGUI does not validate URL schemes because `javascript:` URLs have legitimate uses.
    When accepting URLs from user input, validate the scheme to prevent `javascript:` injection:
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
    **Never do this:**
    ```python
    ui.navigate.to(user_url.value)  # Allows javascript: URL injection!
    ui.link(user_url.value)  # Renders javascript: URLs without validation!
    ```
''')


@doc.demo('CSS Injection', '''
    Element style properties are not escaped because the framework cannot distinguish legitimate CSS
    from [CSS data exfiltration techniques](https://portswigger.net/research/blind-css-exfiltration).
    Validate style values before applying user input:
''')
def css_injection_demo():
    import re

    def is_safe_color(color: str) -> bool:
        hex_pattern = r'^#[0-9a-fA-F]+$'
        rgb_pattern = r'^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$'
        return bool(re.match(hex_pattern, color) or re.match(rgb_pattern, color))

    def apply_color():
        if is_safe_color(user_color.value):
            label.style['color'] = user_color.value
        else:
            ui.notify('Invalid color', type='negative')

    user_color = ui.input('Enter color', placeholder='#0000ff')
    label = ui.label('Sample text')
    ui.button('Apply Color', on_click=apply_color)


doc.text('', '''
    **Never do this:**
    ```python
    label.style['color'] = user_color.value  # Allows CSS injection and data exfiltration
    ```
''')


doc.text('Client-Side Secrets', '''
    NiceGUI assigns each client session a unique `client_id` (a random UUID).

    **Where `client_id` comes from: Pages are the only issuer.**
    Rendering a page mints a fresh `client_id` and embeds it in the response HTML,
    whose elements define what capabilities the `client_id` has.

    - Gate important pages with authentication (middleware redirect, login check, etc.),
    such that unauthenticated visitors never receive a `client_id` that grants access to protected functionality.
    - Besides authentication, guard against side-channel leaks of an authenticated user's HTML (XSS, browser cache exposure).

    **Where `client_id` is consumed: NiceGUI internals under `/_nicegui/`**

    - All internal routes include a `client_id` in their path or query string, and consider it as the session token.
    This includes the Socket.IO transport, the `ui.upload()` POST endpoint, and any other dynamically registered per-client route.
    - There is no separate authentication layer on these routes. Protecting the page that mints the `client_id` is what protects them.

    Hence, a client session is considered **compromised** if either the `client_id` or client-side cookies are exposed to an attacker.

    **To protect client sessions:**

    - **Serve pages over HTTPS** in production to prevent traffic sniffing.
    - **Do not serve untrusted content** from the same origin
      (e.g. serving user-uploaded HTML files could leak secrets via JavaScript).
    - **Do not expose `client_id`** in logs, URLs, or API responses visible to other users.
    - **Treat `client_id` like a session token**: anyone who knows it can send events on behalf of that client.
    - **Secure pages, not `/_nicegui/`**, as the source of the credential is the asset to protect, not the consumer.
''')


doc.text('Examples Are Starting Points', '''
    NiceGUI ships a number of [examples](/examples).
    They demonstrate one specific mechanism (authentication, file upload, terminal, etc.) in the smallest runnable form.
    They are **not** production templates and may intentionally omit hardening that your deployment requires.

    Before using an example as the basis for a real application:

    - **Read every line and understand why it is there.**
      A pattern that is safe in a local demo may be unsafe behind a public URL.
    - **Re-evaluate every threat model assumption.**
      The `xterm` example, for instance, wires a browser to a Bash PTY by design — its purpose is to demo the integration, not to be exposed on the open internet.
    - **Adapt the authentication example to your needs.**
      It illustrates session-based auth at the page level, which is the recommended pattern,
      but production apps typically need rate limiting, CSRF protections beyond the framework's defaults, password hashing, and audit logging — none of which the example provides.
    - **Validate uploaded content server-side.**
      The `ui.upload()` element enforces `max_file_size`, `max_total_size`, and `max_files` in the browser only.
      If your `on_upload` handler writes to disk or processes the file, also validate size and type on the server.
    - **Treat reload mode (`reload=True`) as developer-only.**
      Auto-reload watches the working directory and re-imports changed files. This is convenient locally but unsafe in any environment where untrusted writes can reach that directory.

    Examples are starting points, not finished products.
    Every line of code in your production app is your responsibility.
''')


doc.text('Additional Resources', '''
    **Security Advisories:**

    - [NiceGUI Security Advisories](https://github.com/zauberzeug/nicegui/security/advisories)

    **External Resources:**

    - [OWASP Top 10](https://owasp.org/www-project-top-ten/)
    - [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
    - [DOMPurify](https://github.com/cure53/DOMPurify)

    **Key Principles:**

    1. Keep sanitization enabled (the default)
    2. Validate URL schemes (the framework does not restrict them)
    3. Validate CSS values (the framework does not escape them)
    4. Only disable sanitization for trusted content you control
    5. Apply defense in depth (iframe-blocking headers, input validation)
    6. Keep NiceGUI up to date
''')
