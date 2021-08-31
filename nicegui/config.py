from pydantic import BaseModel
import inspect
import ast
import os

class Config(BaseModel):

    # NOTE: should be in sync with ui.run arguments
    host: str = '0.0.0.0'
    port: int = 80
    title: str = 'NiceGUI'
    favicon: str = 'favicon.ico'
    reload: bool = True
    show: bool = True
    interactive: bool = False


excluded_endings = (
    '<string>',
    'spawn.py',
    'runpy.py',
    os.path.join('debugpy', 'server', 'cli.py'),
    os.path.join('debugpy', '__main__.py'),
)
for f in reversed(inspect.stack()):
    if not any(f.filename.endswith(ending) for ending in excluded_endings):
        filepath = f.filename
        break
else:
    raise Exception("Could not find main script in stacktrace")

try:
    with open(filepath) as f:
        source = f.read()
except FileNotFoundError:
    print('Could not main script. Starting with interactive mode.', flush=True)
    config = Config(interactive=True)
else:
    for node in ast.walk(ast.parse(source)):
        try:
            func = node.value.func
            if func.value.id == 'ui' and func.attr == 'run':
                args = {
                    keyword.arg:
                        keyword.value.n if isinstance(keyword.value, ast.Num) else
                        keyword.value.s if isinstance(keyword.value, ast.Str) else
                        keyword.value.value
                    for keyword in node.value.keywords
                }
                config = Config(**args)
                break
        except AttributeError:
            continue
    else:
        raise Exception('Could not find ui.run() command')

os.environ['HOST'] = config.host
os.environ['PORT'] = str(config.port)
os.environ["STATIC_DIRECTORY"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
os.environ["TEMPLATES_DIRECTORY"] = os.path.join(os.environ["STATIC_DIRECTORY"], 'templates')
