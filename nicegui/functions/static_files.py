from fastapi.staticfiles import StaticFiles

from .. import globals


def add_static_files(path: str, directory: str) -> None:
    """Static Files

    Makes a local directory available at the specified endpoint, e.g. `'/static'`.
    Do only put non-security-critical files in there, as they are accessible to everyone.

    :param path: string that starts with a slash "/"
    :param directory: folder with static files to serve under the given path
    """
    globals.app.mount(path, StaticFiles(directory=directory))
