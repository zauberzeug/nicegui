from nicegui.element import Element


class Fireworks(Element, component='fireworks.vue'):

    def __init__(self, *,
                 gravity: float = 1.4,
                 opacity: float = 0.4,
                 autoresize: bool = True,
                 acceleration: float = 1.0) -> None:
        super().__init__()
        self._props['gravity'] = gravity
        self._props['opacity'] = opacity
        self._props['autoresize'] = autoresize
        self._props['acceleration'] = acceleration

    def start(self):
        self.run_method('startFireworks')

    def stop(self):
        self.run_method('stopFireworks')

    def update_options(self, **kwargs):
        self._props.update(kwargs)
        self.update()
