from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')


def more() -> None:
    @text_demo('Upload restrictions', '''
        In this demo, the upload is restricted to a maximum file size of 1 MB.
        When a file is rejected, a notification is shown.
    ''')
    def upload_restrictions() -> None:
        ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}'),
                  on_rejected=lambda: ui.notify('Rejected!'),
                  max_file_size=1_000_000).classes('max-w-full')
