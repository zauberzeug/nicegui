from nicegui import ui


def main_demo() -> None:
    ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')
