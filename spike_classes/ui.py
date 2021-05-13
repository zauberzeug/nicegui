import justpy as jp
from starlette.applications import Starlette

class Ui(Starlette):

    from elements.label import Label as label
    from elements.button import Button as button

    def __init__(self):
        # NOTE: we enhance our own ui object with all capabilities of jp.app
        self.__dict__.update(jp.app.__dict__)

        self.tasks = []

        @self.on_event('startup')
        def startup():
            [jp.run_task(t) for t in self.tasks]
