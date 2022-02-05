import inspect
import time


def measure(*, reset: bool = False, ms: bool = False):
    global t
    if 't' in globals() and not reset:
        dt = time.time() - t
        line = inspect.stack()[1][0].f_lineno
        output = f'{dt * 1000:7.3f} ms' if ms else f'{dt:7.3f} s'
        print(f'{inspect.stack()[1].filename}:{line}', output, flush=True)
    if reset:
        print('------------', flush=True)
    t = time.time()
