#!/usr/bin/env python3
"""Playwright-based test for the NiceGUI Pyodide demo.

Runs prepare.py, serves the demo via HTTP, opens headless Chromium,
and verifies the page loads and interactive elements work.

Usage:
    python test_pyodide.py [--timeout 120] [--click] [--port 8090] [--no-build]
"""
from __future__ import annotations

import argparse
import http.server
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent
SCREENSHOTS_DIR = DEMO_DIR / 'screenshots'


def start_server(port: int) -> http.server.HTTPServer:
    """Start a plain HTTP server in a background thread."""
    os.chdir(DEMO_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    server = http.server.HTTPServer(('127.0.0.1', port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def navigate(page, link_text: str) -> None:
    """Click a nav link and wait for the sub-page content to render."""
    page.locator(f'a:has-text("{link_text}")').first.click()
    time.sleep(1.5)


def run_test(port: int, timeout: int, click: bool) -> int:
    """Run the Playwright test. Returns exit code (0=success, 1=errors)."""
    from playwright.sync_api import sync_playwright

    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    console_messages: list[dict] = []
    page_errors: list[str] = []
    exit_code = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 960})
        page = context.new_page()

        # Capture console output
        def on_console(msg):
            console_messages.append({'type': msg.type, 'text': msg.text})
            prefix = {'error': 'ERR', 'warning': 'WRN', 'info': 'INF'}.get(msg.type, 'LOG')
            print(f'  [{prefix}] {msg.text}')

        def on_pageerror(error):
            page_errors.append(str(error))
            print(f'  [PAGE_ERROR] {error}')

        page.on('console', on_console)
        page.on('pageerror', on_pageerror)

        url = f'http://127.0.0.1:{port}/'
        print(f'Navigating to {url} ...')
        page.goto(url)

        # Wait for Pyodide to finish loading
        print(f'Waiting for __pyodide_ready (timeout={timeout}s) ...')
        try:
            page.wait_for_function('window.__pyodide_ready === true', timeout=timeout * 1000)
            print('Pyodide ready!')
        except Exception as e:
            print(f'Timeout waiting for Pyodide: {e}')
            exit_code = 1

        # Small extra delay for Vue rendering
        time.sleep(2)

        # Take screenshot
        screenshot_path = SCREENSHOTS_DIR / 'pyodide_test.png'
        page.screenshot(path=str(screenshot_path))
        print(f'Screenshot saved: {screenshot_path}')

        if click:
            # ── Home page test ────────────────────────────────
            print('\n=== Home page ===')
            body_text = page.locator('body').inner_text()
            if 'Navigate using the links above' in body_text:
                print('  Home page content displayed')
            else:
                print('  WARNING: Home page content not visible')
                exit_code = 1

            # Dark mode toggle
            print('Dark mode toggle test ...')
            dark_btn = page.locator('.q-btn .q-icon:has-text("dark_mode")').locator('..')
            if dark_btn.count() > 0:
                dark_btn.click()
                time.sleep(0.5)
                is_dark = page.evaluate('() => document.body.classList.contains("body--dark")')
                if is_dark:
                    print('  Dark mode toggled on')
                else:
                    print('  WARNING: body--dark class not found')
                    exit_code = 1
                # Toggle back off
                dark_btn.click()
                time.sleep(0.5)
                is_light = page.evaluate('() => !document.body.classList.contains("body--dark")')
                if is_light:
                    print('  Dark mode toggled off')
                else:
                    print('  WARNING: body--dark class still present')
                    exit_code = 1
            else:
                print('  WARNING: Dark mode button not found')
                exit_code = 1

            # ══════════════════════════════════════════════════
            # BASICS PAGE
            # ══════════════════════════════════════════════════
            print('\n=== Basics page ===')
            navigate(page, 'Basics')

            # Counter binding
            print('Counter binding test ...')
            inc_btn = page.locator('.q-btn:has-text("+")')
            for _ in range(3):
                inc_btn.click()
                time.sleep(0.3)
            body_text = page.locator('body').inner_text()
            if 'Count: 3' in body_text:
                print('  Counter updated to Count: 3')
            else:
                print('  Expected "Count: 3" in page text')
                exit_code = 1

            # Timer
            print('Timer test ...')
            time.sleep(2)  # wait for at least one tick
            timer_text = page.locator('text=/Elapsed: \\d+s/').first.inner_text()
            elapsed = int(timer_text.split(':')[1].strip().rstrip('s'))
            print(f'  Timer shows: {timer_text} (elapsed={elapsed})')
            if elapsed < 1:
                print('  Timer does not appear to be running')
                exit_code = 1

            # run_javascript
            print('run_javascript test ...')
            page.locator('.q-btn:has-text("GET USER AGENT")').click()
            time.sleep(2)
            result_text = page.locator('text=/Result: .+\\.\\.\\.$/').first.inner_text()
            if 'HeadlessChrome' in result_text or 'Mozilla' in result_text:
                print(f'  run_javascript returned user agent: {result_text[:80]}...')
            else:
                print(f'  Unexpected result: {result_text[:80]}')
                exit_code = 1

            # Notification
            print('Notification test ...')
            page.locator('.q-btn:has-text("SHOW NOTIFICATION")').click()
            time.sleep(1)
            if page.locator('.q-notification').count() > 0:
                print('  Notification appeared')
            else:
                print('  WARNING: notification not found')

            # Async task
            print('Async task test ...')
            page.locator('.q-btn:has-text("RUN ASYNC TASK")').click()
            time.sleep(0.5)
            body_text = page.locator('body').inner_text()
            if 'Async: running...' in body_text:
                print('  Async task started')
            time.sleep(2)
            body_text = page.locator('body').inner_text()
            if 'Async: done!' in body_text:
                print('  Async task completed after sleep')
            else:
                print('  WARNING: Async task did not complete')
                exit_code = 1

            # Refreshable
            print('Refreshable test ...')
            first_color = page.locator('text=/^red|green|blue|orange|purple$/').first.inner_text()
            page.locator('.q-btn:has-text("NEXT COLOR")').click()
            time.sleep(0.5)
            second_color = page.locator('text=/^red|green|blue|orange|purple$/').first.inner_text()
            if first_color != second_color:
                print(f'  Color changed: {first_color} -> {second_color}')
            else:
                print(f'  Color did not change: {first_color}')
                exit_code = 1

            # ══════════════════════════════════════════════════
            # FORMS PAGE
            # ══════════════════════════════════════════════════
            print('\n=== Forms page ===')
            navigate(page, 'Forms')

            # Basic form elements
            print('Form elements test ...')
            input_el = page.locator('.q-input input[type="text"]').first
            input_el.click()
            input_el.fill('Alice')
            time.sleep(0.5)

            slider_el = page.locator('.q-slider').first
            slider_el.click(position={'x': 10, 'y': 10})
            time.sleep(0.5)

            page.locator('.q-checkbox').first.click()
            time.sleep(0.5)

            page.locator('.q-select').first.click()
            time.sleep(0.5)
            page.locator('.q-item:has-text("Option B")').click()
            time.sleep(0.5)

            page.locator('.q-btn:has-text("SHOW FORM VALUES")').click()
            time.sleep(1)

            body_text = page.locator('body').inner_text()
            form_ok = True
            if "name='Alice'" in body_text:
                print('  Input: value updated to Alice')
            else:
                print('  WARNING: Input value not updated')
                form_ok = False
            if 'check=True' in body_text:
                print('  Checkbox: toggled to True')
            else:
                print('  WARNING: Checkbox not toggled')
                form_ok = False
            if "select='Option B'" in body_text:
                print('  Select: picked Option B')
            else:
                print('  WARNING: Select not updated')
                form_ok = False
            slider_match = re.search(r'slider=(\d+)', body_text)
            if slider_match and int(slider_match.group(1)) != 50:
                print(f'  Slider: value changed to {slider_match.group(1)}')
            else:
                print('  WARNING: Slider value unchanged')
                form_ok = False
            if not form_ok:
                exit_code = 1

            # Extra form elements
            print('Extra form elements test ...')
            page.locator('.q-toggle').first.click()
            time.sleep(0.3)
            radio_y = page.locator('.q-radio:has-text("Y")')
            if radio_y.count() > 0:
                radio_y.click()
                time.sleep(0.3)
            toggle_two = page.locator('.q-btn-group .q-btn:has-text("Two")')
            if toggle_two.count() > 0:
                toggle_two.click()
                time.sleep(0.3)
            page.locator('.q-btn:has-text("SHOW EXTRA FORM VALUES")').click()
            time.sleep(1)

            body_text = page.locator('body').inner_text()
            extra_ok = True
            if 'switch=True' in body_text:
                print('  Switch: toggled to True')
            else:
                print('  WARNING: Switch not toggled')
                extra_ok = False
            if "radio='Y'" in body_text:
                print('  Radio: selected Y')
            else:
                print('  WARNING: Radio not updated')
                extra_ok = False
            if "toggle='Two'" in body_text:
                print('  Toggle: selected Two')
            else:
                print('  WARNING: Toggle not updated')
                extra_ok = False
            if not extra_ok:
                exit_code = 1

            # ══════════════════════════════════════════════════
            # CONTENT PAGE
            # ══════════════════════════════════════════════════
            print('\n=== Content page ===')
            navigate(page, 'Content')

            # Markdown
            print('Markdown test ...')
            if page.locator('strong:has-text("Bold")').count() > 0:
                print('  Markdown bold text rendered')
            else:
                print('  WARNING: Markdown bold text not found')
                exit_code = 1
            if page.locator('pre code, code.language-python, .codehilite').count() > 0:
                print('  Markdown code block rendered')
            else:
                print('  WARNING: Markdown code block not found')
                exit_code = 1

            # Table
            print('Table test ...')
            row_count = page.locator('.q-table tbody tr').count()
            if row_count == 3:
                print(f'  Table rendered with {row_count} rows')
            else:
                print(f'  WARNING: Expected 3 table rows, found {row_count}')
                exit_code = 1
            if page.locator('.q-table td:has-text("Alice")').count() > 0:
                print('  Table contains "Alice" cell')
            else:
                print('  WARNING: Table cell "Alice" not found')
                exit_code = 1

            # Tabs
            print('Tabs test ...')
            tab_b_el = page.locator('.q-tab:has-text("Tab B")')
            if tab_b_el.count() > 0:
                tab_b_el.click()
                time.sleep(0.5)
                body_text = page.locator('body').inner_text()
                if 'Content of Tab B' in body_text:
                    print('  Tab B content visible after click')
                else:
                    print('  WARNING: Tab B content not visible')
                    exit_code = 1
                if 'Tab: Tab B' in body_text:
                    print('  Tab on_value_change handler fired')
                else:
                    print('  WARNING: Tab value change handler did not fire')
                    exit_code = 1
            else:
                print('  WARNING: Tab B element not found')
                exit_code = 1

            # Dialog
            print('Dialog test ...')
            page.locator('.q-btn:has-text("OPEN DIALOG")').click()
            time.sleep(1)
            dialog_card = page.locator('.q-dialog .q-card')
            if dialog_card.count() > 0:
                if 'Hello from dialog' in dialog_card.inner_text():
                    print('  Dialog opened with correct content')
                else:
                    print('  WARNING: Dialog content unexpected')
                    exit_code = 1
                page.locator('.q-dialog .q-btn:has-text("CLOSE")').click()
                time.sleep(0.5)
            else:
                print('  WARNING: Dialog did not appear')
                exit_code = 1
            if 'Dialog: opened' in page.locator('body').inner_text():
                print('  Dialog on_click handler fired')
            else:
                print('  WARNING: Dialog on_click handler did not fire')
                exit_code = 1

            # Expansion
            print('Expansion test ...')
            expansion = page.locator('.q-expansion-item')
            if expansion.count() > 0:
                expansion.first.click()
                time.sleep(0.5)
                if 'Hidden content revealed' in page.locator('body').inner_text():
                    print('  Expansion item opened, content visible')
                else:
                    print('  WARNING: Expansion content not visible')
                    exit_code = 1
            else:
                print('  WARNING: Expansion item not found')
                exit_code = 1

            # Tooltip
            print('Tooltip test ...')
            tooltip_btn = page.locator('.q-btn:has-text("HOVER ME")')
            if tooltip_btn.count() > 0:
                tooltip_btn.hover()
                time.sleep(1)
                if page.locator('.q-tooltip').count() > 0:
                    print('  Tooltip appeared on hover')
                else:
                    print('  WARNING: Tooltip not visible')

            # Badge
            print('Badge test ...')
            badge = page.locator('.q-badge')
            if badge.count() > 0 and badge.first.inner_text() == '3':
                print('  Badge rendered with text "3"')
            else:
                print('  WARNING: Badge not found')
                exit_code = 1

            # Image
            print('Image test ...')
            if page.locator('img[src^="data:image"]').count() > 0:
                print('  Data URI image rendered')
            else:
                print('  WARNING: Data URI image not found')
                exit_code = 1

            # Mermaid diagram
            print('Mermaid diagram test ...')
            mermaid_svg = page.locator('svg[id*=mermaid]')
            try:
                mermaid_svg.first.wait_for(state='visible', timeout=15000)
                print('  Mermaid SVG rendered successfully')
            except Exception:
                print('  WARNING: Mermaid SVG not rendered in time')
                exit_code = 1

            # Mermaid node click
            print('Mermaid node click test ...')
            nodes = page.locator('svg[id*=mermaid] g.node')
            if nodes.count() > 0:
                nodes.first.click()
                time.sleep(1)
                body_text = page.locator('body').inner_text()
                match = re.search(r'Clicked: (\S+)', body_text)
                if match:
                    print(f'  Node click handler fired: {match.group(0)}')
                else:
                    print('  WARNING: Mermaid node click did not trigger handler')
                    exit_code = 1
            else:
                print('  WARNING: No g.node elements found')
                exit_code = 1

            # ══════════════════════════════════════════════════
            # I/O PAGE
            # ══════════════════════════════════════════════════
            print('\n=== I/O page ===')
            navigate(page, 'I/O')

            # Upload
            print('Upload test ...')
            file_input = page.locator('.q-uploader input[type="file"]')
            if file_input.count() > 0:
                file_input.set_input_files({
                    'name': 'test.txt',
                    'mimeType': 'text/plain',
                    'buffer': b'Hello from Playwright!',
                })
                time.sleep(2)
                body_text = page.locator('body').inner_text()
                if 'Received "test.txt"' in body_text and '22 bytes' in body_text:
                    print('  Upload handler received file correctly')
                else:
                    print('  Upload result not found in page text')
                    exit_code = 1
            else:
                print('  WARNING: Upload file input not found')
                exit_code = 1

            # ══════════════════════════════════════════════════
            # SPA NAVIGATION TEST
            # ══════════════════════════════════════════════════
            print('\n=== SPA navigation test ===')
            navigate(page, 'Home')
            if 'Navigate using the links above' in page.locator('body').inner_text():
                print('  Navigated back to Home')
            else:
                print('  WARNING: Home page not visible after navigation')
                exit_code = 1

            # Final screenshot
            final_path = SCREENSHOTS_DIR / 'pyodide_test_final.png'
            page.screenshot(path=str(final_path))
            print(f'\nFinal screenshot saved: {final_path}')

        browser.close()

    # Summary
    print('\n=== SUMMARY ===')
    error_count = len([m for m in console_messages if m['type'] == 'error']) + len(page_errors)
    print(f'Console messages: {len(console_messages)}')
    print(f'Errors: {error_count}')
    print(f'Page errors: {len(page_errors)}')
    if page_errors:
        exit_code = 1
        for err in page_errors:
            print(f'  PAGE_ERROR: {err}')

    return exit_code


def main():
    parser = argparse.ArgumentParser(description='Test NiceGUI Pyodide demo')
    parser.add_argument('--timeout', type=int, default=120, help='Timeout in seconds for Pyodide load')
    parser.add_argument('--click', action='store_true', help='Test button clicks after load')
    parser.add_argument('--port', type=int, default=8090, help='HTTP server port')
    parser.add_argument('--no-build', action='store_true', help='Skip building the wheel (pass to prepare.py)')
    args = parser.parse_args()

    # Run prepare.py to copy/build assets
    prepare_cmd = [sys.executable, str(DEMO_DIR / 'prepare.py')]
    if args.no_build:
        prepare_cmd.append('--no-build')
    print('Running prepare.py ...')
    subprocess.run(prepare_cmd, check=True)

    server = start_server(args.port)
    try:
        exit_code = run_test(args.port, args.timeout, args.click)
    finally:
        server.shutdown()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
