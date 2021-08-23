import justpy as jp
from .element import Element
import asyncio


class Notify(Element):

    def __init__(self,
                 message: str,
                 *,
                 position: str = 'bottom',
                 close_button: str = None
                 ):
        """Notification

        Displays a notification on the screen.

        :param message: content of the notification
        :param position: position on the screen ("top-left", "top-right", "bottom-left","bottom-right, "top", "bottom", "left", "right" or "center", default: "bottom")
        :param close_button: optional label of a button to dismiss the notification (default: None)
        """

        view = jp.QNotify(message=message, position=position, closeBtn=close_button)

        super().__init__(view)
        asyncio.get_event_loop().create_task(self.notify_async())

    async def notify_async(self):

        self.view.notify = True
        await self.parent_view.update()
        self.view.notify = False
