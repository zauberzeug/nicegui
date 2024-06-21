from nicegui import ui

from . import doc


@doc.demo(ui.upload)
def main_demo() -> None:
    ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')


@doc.demo('Upload restrictions', '''
    In this demo, the upload is restricted to a maximum file size of 1 MB.
    When a file is rejected, a notification is shown.
''')
def upload_restrictions() -> None:
    ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}'),
              on_rejected=lambda: ui.notify('Rejected!'),
              max_file_size=1_000_000).classes('max-w-full')


@doc.demo('Show file content', '''
    In this demo, the uploaded markdown file is shown in a dialog.
''')
def show_file_content() -> None:
    from nicegui import events

    with ui.dialog().props('full-width') as dialog:
        with ui.card():
            content = ui.markdown()

    def handle_upload(e: events.UploadEventArguments):
        text = e.content.read().decode('utf-8')
        content.set_content(text)
        dialog.open()

    ui.upload(on_upload=handle_upload).props('accept=.md').classes('max-w-full')


@doc.demo('Uploading large files', '''
    Large file uploads may encounter issues due to the default file size parameter set within the underlying Starlette library.
    To ensure smooth uploads of larger files, it is recommended to increase the `max_file_size` parameter in Starlette's `MultiPartParser` class from the default of `1024 * 1024` (1 MB) to a higher limit that aligns with the expected file sizes.

    This demo increases Starlette Multiparser's `max_file_size` to be kept in RAM to 5 MB.
    This change allows the system to handle larger files more efficiently by keeping them in RAM, thus avoiding the need to write data to temporary files on disk and preventing upload "stuttering".

    However, be mindful of the potential impact on your server when allowing users to upload large files and retaining them in RAM.
''')
def uploading_large_files() -> None:
    from starlette.formparsers import MultiPartParser

    MultiPartParser.max_file_size = 1024 * 1024 * 5  # 5 MB

    ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')


doc.reference(ui.upload)
