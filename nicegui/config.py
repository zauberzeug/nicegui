from pydantic import BaseModel
import inspect
import ast
import os

class Config(BaseModel):

    # NOTE: should be in sync with ui.run arguments
    host: str = '0.0.0.0'
    port: int = 80
    title: str = 'NiceGUI'
    favicon: str = 'favicon.png'
    reload: bool = True
    show: bool = True


endings = ('<string>', 'spawn.py', 'runpy.py', 'debugpy/server/cli.py', 'debugpy/__main__.py')
for f in reversed(inspect.stack()):
    if not any(f.filename.endswith(ending) for ending in endings):
        filepath = f.filename
        break
else:
    raise Exception("Could not find main script in stacktrace")

with open(filepath) as f:
    source = f.read()

for node in ast.parse(source).body:
    try:
        func = node.value.func
        if func.value.id == 'ui' and func.attr == 'run':
            args = {
                keyword.arg: keyword.value.value
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
os.environ["STATIC_DIRECTORY"] = os.path.dirname(os.path.realpath(__file__)) + '/static'
os.environ["TEMPLATES_DIRECTORY"] = os.environ["STATIC_DIRECTORY"] + '/templates'
