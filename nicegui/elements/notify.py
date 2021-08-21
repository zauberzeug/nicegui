import justpy as jp
from .element import Element
import asyncio


class Notify(Element):

    def __init__(self,
                 message: str = '',
                 position: str = 'bottom',
                 close_button: str = ''
                 ):
        """Notification Element

        Displays a notification on the screen.

        :param message: the content of the notification
        :param position: possible position: 'top-left', 'top-right', 'bottom-left','bottom-right, 'top', 'bottom', 'left', 'right', 'center'
        :param close_button: label of the button to dismiss the notification
        """

        view = jp.QNotify(message=message, position=position)

        if close_button:
            view.closeBtn = close_button

        super().__init__(view)
        asyncio.get_event_loop().create_task(self.notify_async())

    async def notify_async(self):
        self.view.notify = True
        await self.parent_view.update()
        self.view.notify = False
