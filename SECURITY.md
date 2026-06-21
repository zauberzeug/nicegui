# Security Policy

Security is very important for NiceGUI and its community. 🔒

Learn more about it below. 👇

## Versions

The latest version of NiceGUI is supported.

You are encouraged to write tests for your application and update your NiceGUI version frequently after ensuring that your tests are passing.
This way you will benefit from the latest features, bug fixes, and **security fixes**.

## Commonly Misreported Patterns

Automated scanners and AI-assisted reviews frequently flag the patterns below.
They are **by design or already bounded**, so please trace the data flow and check them against this list before filing — it keeps the advisory queue focused on real issues.

- **`| safe` in the page template** (`nicegui/templates/index.html`). Jinja auto-escaping is bypassed there intentionally; the values are escaped at the source instead (for example, element data is escaped with a table sized for the `String.raw` script context it lands in). A bare `| safe` is not itself a finding — trace where the value comes from and how it is escaped.
- **Raw `innerHTML` in `ui.html` / `ui.markdown`** (`nicegui/elements/html.js`, `markdown.js`). The raw assignment is the `else` branch of `sanitize`: the opt-in `sanitize=False` path. The default (`sanitize=True`) sanitizes via DOMPurify. Passing untrusted input with `sanitize=False` is the caller's documented responsibility.
- **`ui.add_head_html`, `ui.add_body_html`, `ui.run_javascript`, `ui.add_css`.** These inject raw HTML/JS/CSS by design and are documented as never-for-untrusted-input. Using them with unsanitized user data is an application bug, not a framework vulnerability.
- **`ast.literal_eval` in the docs.** `literal_eval` only parses literals; it is the safe alternative to `eval` that the documentation demonstrates.

If instead you have found a way **around** one of these protections — an escaping bypass, or a default `sanitize=True` path that still executes script — that is a real issue and we would very much like to hear about it. Please include a reproduction.

## Reporting a Vulnerability

If you think you found a vulnerability, and even if you are not sure about it, please report it right away
by creating a private security advisory (GitHub → Security → Report a vulnerability)
so we can discuss and patch the issue in a secure workspace.
If you cannot use GitHub, you can also send an email to: nicegui@zauberzeug.com.

Please try to be as explicit as possible, describing all the steps and example code to reproduce the security issue.

We (the team at Zauberzeug) will review it thoroughly and get back to you.

## Public Discussions

Please restrain from publicly discussing a potential security vulnerability. 🙊

It's better to discuss privately and try to find a solution first, to limit the potential impact as much as possible.

---

Thanks for your help!

The NiceGUI community and the Zauberzeug team thank you for that. 🙇
