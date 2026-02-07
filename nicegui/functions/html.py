import re

from ..client import Client
from ..context import context


def _inject_nonce_to_html(html: str, nonce: str) -> str:
    """Inject nonce attribute to inline script and style tags that don't already have it."""
    if not nonce:
        return html

    # Add nonce to <script> tags that don't have external src or nonce already
    html = re.sub(
        r'<script\b(?![^>]*\bnonce=)(?![^>]*\bsrc=)([^>]*)>',
        rf'<script nonce="{nonce}"\1>',
        html,
        flags=re.IGNORECASE
    )

    # Add nonce to <style> tags that don't already have nonce
    html = re.sub(
        r'<style\b(?![^>]*\bnonce=)([^>]*)>',
        rf'<style nonce="{nonce}"\1>',
        html,
        flags=re.IGNORECASE
    )

    return html


def add_head_html(code: str, *, shared: bool = False) -> None:
    """Add HTML code to the head of the page.

    :param code: HTML code to add
    :param shared: if True, the code is added to all pages
    """
    if shared:
        Client.shared_head_html += code + '\n'
    else:
        client = context.client
        if client.has_socket_connection:
            # Get CSP nonce from client (stored during build_response)
            nonce = getattr(client, '_csp_nonce', '')
            code_with_nonce = _inject_nonce_to_html(code, nonce)
            # Use a helper function that properly handles CSP nonces for dynamic insertion
            client.run_javascript(f'''
                (() => {{
                    const template = document.createElement('template');
                    template.innerHTML = {code_with_nonce!r};
                    const nodes = Array.from(template.content.childNodes);
                    nodes.forEach(node => {{
                        if (node.nodeType === Node.ELEMENT_NODE) {{
                            // For script and style elements, we need to clone them properly to respect nonces
                            if (node.tagName === 'SCRIPT' || node.tagName === 'STYLE') {{
                                const newNode = document.createElement(node.tagName.toLowerCase());
                                Array.from(node.attributes).forEach(attr => {{
                                    newNode.setAttribute(attr.name, attr.value);
                                }});
                                newNode.textContent = node.textContent;
                                document.head.appendChild(newNode);
                            }} else {{
                                document.head.appendChild(node);
                            }}
                        }} else {{
                            document.head.appendChild(node);
                        }}
                    }});
                }})();
            '''.strip())
        # Don't inject nonce here - it will be injected at render time in build_response
        client._head_html += code + '\n'  # pylint: disable=protected-access


def add_body_html(code: str, *, shared: bool = False) -> None:
    """Add HTML code to the body of the page.

    :param code: HTML code to add
    :param shared: if True, the code is added to all pages
    """
    if shared:
        Client.shared_body_html += code + '\n'
    else:
        client = context.client
        if client.has_socket_connection:
            # Get CSP nonce from client (stored during build_response)
            nonce = getattr(client, '_csp_nonce', '')
            code_with_nonce = _inject_nonce_to_html(code, nonce)
            # Use a helper function that properly handles CSP nonces for dynamic insertion
            client.run_javascript(f'''
                (() => {{
                    const template = document.createElement('template');
                    template.innerHTML = {code_with_nonce!r};
                    const nodes = Array.from(template.content.childNodes);
                    const app = document.querySelector("#app");
                    nodes.forEach(node => {{
                        if (node.nodeType === Node.ELEMENT_NODE) {{
                            // For script and style elements, we need to clone them properly to respect nonces
                            if (node.tagName === 'SCRIPT' || node.tagName === 'STYLE') {{
                                const newNode = document.createElement(node.tagName.toLowerCase());
                                Array.from(node.attributes).forEach(attr => {{
                                    newNode.setAttribute(attr.name, attr.value);
                                }});
                                newNode.textContent = node.textContent;
                                app.insertAdjacentElement("beforebegin", newNode);
                            }} else {{
                                app.insertAdjacentElement("beforebegin", node);
                            }}
                        }} else {{
                            app.insertAdjacentElement("beforebegin", node);
                        }}
                    }});
                }})();
            '''.strip())
        # Don't inject nonce here - it will be injected at render time in build_response
        client._body_html += code + '\n'  # pylint: disable=protected-access
