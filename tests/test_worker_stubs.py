import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import pytest

EXAMPLES = Path(__file__).resolve().parent.parent / 'examples'

WORKER_CODE = dedent('''\
    import os, sys, time
    os.environ['NICEGUI_WORKER_STUBS'] = '1'
    import multiprocessing as mp

    def child(queue):
        t0 = time.perf_counter()
        import nicegui
        from nicegui import ui, app
        elapsed_ms = (time.perf_counter() - t0) * 1000
        from nicegui import run  # what unpickling a cpu_bound payload triggers; must be the REAL module
        label = ui.label('hello')          # must be a no-op
        with ui.row():                     # context manager must work
            ui.button('x')
        ui.run()                           # must be a no-op
        queue.put({
            'elapsed_ms': elapsed_ms,
            'ui_is_stub': type(sys.modules['nicegui.ui']).__name__ == 'WhateverModule',
            'run_is_real': type(sys.modules['nicegui.run']).__name__ != 'WhateverModule',
            'cpu_bound_callable': callable(run.cpu_bound) and run.cpu_bound.__name__ == 'cpu_bound',
            'fastapi_loaded': 'fastapi' in sys.modules,
        })

    if __name__ == '__main__':
        ctx = mp.get_context('spawn')
        q = ctx.Queue()
        p = ctx.Process(target=child, args=(q,))
        p.start()
        result = q.get(timeout=30)
        p.join()
        print(result)
        assert result['ui_is_stub'], 'ui must be stubbed in worker'
        assert result['run_is_real'], 'run must be the real module in worker'
        assert result['cpu_bound_callable'], 'run.cpu_bound must be the real function in worker'
        assert not result['fastapi_loaded'], 'fastapi must not load in worker'
        assert result['elapsed_ms'] < 500, f"stub import took {result['elapsed_ms']:.1f} ms"
''')


def test_worker_gets_stubs(tmp_path):
    script = tmp_path / 'worker_app.py'
    script.write_text(WORKER_CODE)
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=60, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


# The goal function (#5684): when an official example spawns a worker, re-importing the example module must NOT
# pull in the web framework. 'progress' defines its UI inside @ui.page; 'menu_and_tabs' defines it at module level
# with `with ui.x():` blocks — between them they cover both idiomatic shapes, each ending in a bare ui.run().
@pytest.mark.parametrize('example', ['progress', 'menu_and_tabs'])
def test_official_example_worker_reimport_is_framework_free(example, tmp_path):
    example_main = EXAMPLES / example / 'main.py'
    assert example_main.is_file(), f'missing example: {example_main}'
    driver = tmp_path / 'driver.py'
    driver.write_text(dedent(f'''\
        import os, sys, runpy, multiprocessing as mp
        os.environ['NICEGUI_WORKER_STUBS'] = '1'

        def worker(q):
            try:
                runpy.run_path({str(example_main)!r}, run_name='__mp_main__')  # what mp.spawn does to the user's main
            except SystemExit:
                pass
            q.put({{'fastapi': 'fastapi' in sys.modules,
                    'ui_is_stub': type(sys.modules.get('nicegui.ui')).__name__ == 'WhateverModule'}})

        if __name__ == '__main__':
            ctx = mp.get_context('spawn')
            q = ctx.Queue()
            p = ctx.Process(target=worker, args=(q,))
            p.start(); print(q.get(timeout=60)); p.join()
    '''))
    result = subprocess.run([sys.executable, str(driver)], capture_output=True, text=True, timeout=90, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    out = eval(result.stdout.strip().splitlines()[-1])  # pylint: disable=eval-used
    assert out['ui_is_stub'], f'{example}: ui must be stubbed in the worker'
    assert not out['fastapi'], f'{example}: re-importing the example in a worker must not import fastapi'


def test_fresh_main_process_never_stubbed():
    code = dedent('''\
        import os, sys
        os.environ['NICEGUI_WORKER_STUBS'] = '1'  # even with the marker present...
        import nicegui                              # ...a fresh MainProcess must get the real package
        from nicegui import ui
        assert type(sys.modules['nicegui.ui']).__name__ != 'WhateverModule'
        assert ui.label.__name__ == 'Label'
    ''')
    result = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_marker_not_set_means_real_import_in_child(tmp_path):
    script = tmp_path / 'no_marker_app.py'
    script.write_text(dedent('''\
        import multiprocessing as mp
        import os
        import sys
        os.environ.pop('NICEGUI_WORKER_STUBS', None)  # the surrounding pytest process may have it set

        def child(queue):
            import nicegui
            queue.put(type(sys.modules.get('nicegui.ui', None)).__name__ if 'nicegui.ui' in sys.modules else 'unloaded')

        if __name__ == '__main__':
            ctx = mp.get_context('spawn')
            q = ctx.Queue()
            p = ctx.Process(target=child, args=(q,))
            p.start()
            assert q.get(timeout=30) != 'WhateverModule'
            p.join()
    '''))
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=60, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
