#!/usr/bin/env python3
"""Fast offline test for NiceGUI Pyodide import chain.

Simulates a Pyodide environment by blocking server modules, then tests
that `from nicegui import Client, ui` works without errors.

Usage:
    python examples/pyodide/test_pyodide_import.py
"""
from __future__ import annotations

import json
import sys
import types

# === Step 1: Block all server modules to simulate Pyodide ===
BLOCKED_MODULES = [
    'fastapi', 'fastapi.responses', 'fastapi.templating', 'fastapi.middleware',
    'starlette', 'starlette.middleware', 'starlette.middleware.base',
    'starlette.middleware.sessions', 'starlette.requests', 'starlette.responses',
    'starlette.routing', 'starlette.datastructures', 'starlette.staticfiles',
    'uvicorn', 'uvicorn.supervisors',
    'socketio', 'engineio',
    'aiofiles', 'anyio',
    'ifaddr',
    'orjson',
    'httpx',
    'python_multipart',
    '_multiprocessing',  # removed from Pyodide
]


class BlockedModuleError(ImportError):
    pass


class BlockedModuleFinder:
    """Meta path finder that blocks specific modules to simulate Pyodide."""

    def __init__(self, blocked: list[str]):
        self._blocked = set(blocked)

    def find_module(self, fullname: str, path=None):
        # Block exact matches and submodules
        for blocked in self._blocked:
            if fullname == blocked or fullname.startswith(blocked + '.'):
                return self
        return None

    def load_module(self, fullname: str):
        raise BlockedModuleError(f"No module named '{fullname}' (blocked to simulate Pyodide)")


# Install the blocker BEFORE any nicegui imports
blocker = BlockedModuleFinder(BLOCKED_MODULES)
sys.meta_path.insert(0, blocker)

# === Step 2: Fake being in Pyodide ===
fake_pyodide = types.ModuleType('pyodide')
fake_pyodide.__path__ = []
sys.modules['pyodide'] = fake_pyodide


def run_test():
    print('=== NiceGUI Pyodide Import Test ===\n')

    # Step 3: Test basic import
    print('1. Importing nicegui ...')
    try:
        from nicegui import Client, ui
        print('   OK: Client and ui imported successfully')
    except Exception as e:
        print(f'   FAIL: {e}')
        import traceback
        traceback.print_exc()
        return 1

    # Step 4: Test page_pyodide import
    print('2. Importing page_pyodide ...')
    try:
        from nicegui.page_pyodide import page
        print('   OK: page imported from page_pyodide')
    except Exception as e:
        print(f'   FAIL: {e}')
        import traceback
        traceback.print_exc()
        return 1

    # Step 5: Test element creation
    print('3. Creating elements ...')
    try:
        with Client(page('')) as client:
            ui.label('Hello from simulated Pyodide!')
            ui.button('Click me!')
        element_count = len(client.elements)
        print(f'   OK: Created {element_count} elements')
    except Exception as e:
        print(f'   FAIL: {e}')
        import traceback
        traceback.print_exc()
        return 1

    # Step 6: Test serialization
    print('4. Serializing elements ...')
    try:
        data = {
            str(eid): element._to_dict()
            for eid, element in client.elements.items()
        }
        json_str = json.dumps(data, indent=2)
        print(f'   OK: Serialized {len(data)} elements ({len(json_str)} chars)')
    except Exception as e:
        print(f'   FAIL: {e}')
        import traceback
        traceback.print_exc()
        return 1

    # Step 7: Test component collection (for Pyodide component loading)
    print('5. Testing component collection ...')
    try:
        from nicegui.dependencies import JsComponent
        from nicegui.pyodide.runtime import ELEMENTS_DIR

        with Client(page('')) as client2:
            ui.label('test')
            ui.mermaid('graph LR\n    A --> B')

        seen: set[str] = set()
        components = []
        for element in client2.elements.values():
            comp = element.component
            if not isinstance(comp, JsComponent) or comp.name in seen:
                continue
            seen.add(comp.name)
            try:
                rel = comp.path.relative_to(ELEMENTS_DIR)
            except ValueError:
                continue
            components.append({'url': f'./components/{rel}', 'tag': comp.tag})

        print(f'   OK: Found {len(components)} components to load:')
        for c in components:
            print(f'       {c["tag"]} -> {c["url"]}')
        if not any(c['tag'] == 'nicegui-mermaid' for c in components):
            print('   FAIL: Expected nicegui-mermaid component')
            return 1
    except Exception as e:
        print(f'   FAIL: {e}')
        import traceback
        traceback.print_exc()
        return 1

    print('\n=== ALL TESTS PASSED ===')
    return 0


if __name__ == '__main__':
    sys.exit(run_test())
