from . import globals
from .task_logger import create_task


def notify(message: str, *,
           type: str = '',
           color: str = '',
           ) -> None:
    options = {key: value for key, value in locals().items() if not key.startswith('_')}
    create_task(globals.sio.emit('notify', options, room=str(globals.client_stack[-1].id)))
