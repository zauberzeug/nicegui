from typing import Optional, Sequence, Union

from ..context import context
from ..events import GenericEventArguments, Handler


def on(type: str,  # pylint: disable=redefined-builtin
       handler: Optional[Handler[GenericEventArguments]] = None,
       args: Union[None, Sequence[str], Sequence[Optional[Sequence[str]]]] = None, *,
       throttle: float = 0.0,
       leading_events: bool = True,
       trailing_events: bool = True,
       ):
    """Subscribe to a global event.

    :param type: name of the event
    :param handler: callback that is called upon occurrence of the event
    :param args: arguments included in the event message sent to the event handler (default: `None` meaning all)
    :param throttle: minimum time (in seconds) between event occurrences (default: 0.0)
    :param leading_events: whether to trigger the event handler immediately upon the first event occurrence (default: `True`)
    :param trailing_events: whether to trigger the event handler after the last event occurrence (default: `True`)
    """
    context.client.layout.on(type, handler, args,
                             throttle=throttle, leading_events=leading_events, trailing_events=trailing_events)
