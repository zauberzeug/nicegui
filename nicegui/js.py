from pathlib import Path
from typing import Optional

from .nicegui import app

# values should match ones in static/nicegui.js
NEED_TO_EVAL = '_nicegui_need_to_eval_:'
NEED_TO_IMPORT = '_nicegui_need_to_import_:'


class js(str):

    def __new__(cls, obj: str, file: Optional[Path] = None):
        val: str
        if file:
            file_resolved = file.resolve()
            assert file_resolved.is_file() and file_resolved.suffix == '.js', f'{file_resolved} is not a .js file.'
            app.add_static_file(local_file=file_resolved, url_path=f'/user-static-js/{file.stem}')
            val = f'{NEED_TO_IMPORT}{{"url": "/user-static-js/{file.stem}", "obj": "{obj}"}}'
        else:
            val = f'{NEED_TO_EVAL}{obj}'
        return str.__new__(cls, val)
