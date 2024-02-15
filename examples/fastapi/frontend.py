from fastapi import FastAPI

from nicegui import app, ui


def init(fastapi_app: FastAPI) -> None:
    """
    Initialize the NiceGUI frontend for FastAPI.

    This function sets up the NiceGUI frontend for a FastAPI application. It defines a route
    for the root URL ("/") and binds a UI page to it. The UI page displays a label with the
    message "Hello, FastAPI!" and provides a checkbox to toggle dark mode.

    The dark mode setting is persistent for each user across tabs and server restarts. It is
    stored in the `app.storage.user` dictionary under the key 'dark_mode'. The checkbox is
    bound to this value, so changing the checkbox will update the dark mode setting.

    Parameters:
    - fastapi_app (FastAPI): The FastAPI application instance.

    Returns:
    - None

    Example usage:
    ```
    from fastapi import FastAPI
    from nicegui.examples.fastapi import frontend

    app = FastAPI()

    frontend.init(app)

    # ... add your FastAPI routes and logic ...

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    ```
    """

    @ui.page('/')
    def show():
        ui.label('Hello, FastAPI!')

        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')

    ui.run_with(
        fastapi_app,
        mount_path='/gui',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
    )
