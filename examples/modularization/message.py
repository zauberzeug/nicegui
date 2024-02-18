from nicegui import ui


class message(ui.label):

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.classes('text-h4 text-grey-8')
