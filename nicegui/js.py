from .nicegui import app
from typing import Optional
from pathlib import Path


class js(str):

    def __new__(cls, obj: str, file: Optional[Path] = None, prop: Optional[str] = None):
        val: str
        if file:
            file_resolved = file.resolve()
            assert file_resolved.is_file() and file_resolved.suffix == ".js", f"{file_resolved} is not a .js file."
            app.add_static_file(local_file=file_resolved, url_path=f"/user-static-js/{file.stem}")
            val = f'_nicegui_js_import:{{"url": "/user-static-js/{file.stem}", "obj": "{obj}", "prop": "{prop or obj}"}}'
        else:
            val = f"_nicegui_need_to_eval_:{obj}"
        return str.__new__(cls, val)