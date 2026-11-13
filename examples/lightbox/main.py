#!/usr/bin/env python3
from nicegui import events, ui


class Lightbox:
    """A thumbnail gallery where each image can be clicked to enlarge.
    Inspired by https://lokeshdhakar.com/projects/lightbox2/.
    """

    def __init__(self) -> None:
        with ui.dialog().props('maximized').classes('bg-black') as self.dialog:
            ui.keyboard(self._handle_key)
            self.large_image = ui.image().props('no-spinner fit=scale-down')
        self.image_list: list[str] = []

    def add_image(self, thumb_url: str, orig_url: str) -> ui.image:
        """Place a thumbnail image in the UI and make it clickable to enlarge."""
        self.image_list.append(orig_url)
        with ui.button(on_click=lambda: self._open(orig_url)).props('flat dense square'):
            return ui.image(thumb_url)

    def _handle_key(self, event_args: events.KeyEventArguments) -> None:
        if not event_args.action.keydown:
            return
        if event_args.key.escape:
            self.dialog.close()
        image_index = self.image_list.index(self.large_image.source)
        if event_args.key.arrow_left and image_index > 0:
            self._open(self.image_list[image_index - 1])
        if event_args.key.arrow_right and image_index < len(self.image_list) - 1:
            self._open(self.image_list[image_index + 1])

    def _open(self, url: str) -> None:
        self.large_image.set_source(url)
        self.dialog.open()


@ui.page('/')
def page():
    lightbox = Lightbox()
    with ui.row().classes('w-full'):
        for name in ['valley', 'mug', 'feet', 'bench', 'drops', 'sea', 'bridge', 'night', 'birds', 'grapes', 'hikers']:
            # the lightbox allows us to add images which can be opened in a full screen dialog
            lightbox.add_image(
                thumb_url=f'https://nicegui.io/images/{name}/300/200',
                orig_url=f'https://nicegui.io/images/{name}/1200/800',
            ).classes('w-[300px] h-[200px]')


ui.run()
