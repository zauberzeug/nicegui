#!/usr/bin/env python3
"""Example demonstrating Content Security Policy (CSP) support in NiceGUI.

CSP is a security feature that helps prevent XSS attacks by controlling which resources
can be loaded and executed on a page.

IMPORTANT LIMITATIONS:
- Dynamic HTML injection via ui.add_head_html() or ui.add_body_html() during event handlers
  will NOT work with CSP enabled, as browsers reject dynamically-set nonces for security reasons
- If you need dynamic HTML injection, keep CSP disabled (the default)
- CSP is best suited for static pages or pages where all HTML is known at build time
"""
from nicegui import app, ui


# Enable CSP by setting the config option
app.config.csp_enabled = True

# Optionally add custom CSP directives
# app.config.csp_extra_directives = ["connect-src 'self' https://api.example.com"]


@ui.page('/')
def index():
    ui.label('CSP Example').classes('text-2xl')
    ui.label('This page has CSP enabled!')

    # Static HTML added during page build works fine with CSP
    ui.add_head_html('<style>.csp-test {color: green; font-weight: bold;}</style>')
    ui.label('This text uses a style added via add_head_html()').classes('csp-test')

    # External scripts and styles work fine with CSP
    ui.button('Test Button', on_click=lambda: ui.notify('Button clicked!'))

    ui.markdown('''
    ### CSP Configuration

    CSP is configured in your app startup code:

    ```python
    from nicegui import app

    # Enable CSP
    app.config.csp_enabled = True

    # Add custom directives (optional)
    app.config.csp_extra_directives = [
        "connect-src 'self' https://api.example.com",
        "frame-ancestors 'none'"
    ]
    ```

    ### Current CSP Policy

    The default CSP policy includes:
    - `script-src 'nonce-XXX' 'strict-dynamic'` - Only allow scripts with the correct nonce
    - `style-src 'self' 'nonce-XXX' 'unsafe-inline'` - Allow styles from same origin and with nonce
    - `font-src 'self' data:` - Allow fonts from same origin and data URIs
    - `img-src 'self' data: https:` - Allow images from same origin, data URIs, and HTTPS
    - `object-src 'none'` - Block plugins like Flash
    - `base-uri 'none'` - Prevent base tag hijacking

    ### Limitations

    ⚠️ **Dynamic HTML injection does not work with CSP enabled!**

    The following will NOT work when CSP is enabled:
    - Adding HTML via ui.add_head_html() or ui.add_body_html() in event handlers
    - Dynamically creating inline scripts or styles via JavaScript

    This is a fundamental browser security limitation - dynamically set nonces are ignored.
    ''')


if __name__ == '__main__':
    ui.run()
