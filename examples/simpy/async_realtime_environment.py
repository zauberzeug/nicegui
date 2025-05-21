import asyncio
from time import monotonic
from typing import Any, Optional, Union

from simpy.core import EmptySchedule, Environment, Infinity, SimTime, StopSimulation
from simpy.events import URGENT, Event
from simpy.rt import RealtimeEnvironment


class AsyncRealtimeEnvironment(RealtimeEnvironment):
    """A real-time simulation environment that uses asyncio.

    The methods step and run are a 1-1 copy of the original methods from simpy.rt.RealtimeEnvironment,
    except that they are async and await asyncio.sleep instead of time.sleep.
    """

    async def step(self) -> None:
        """Process the next event after enough real-time has passed for the
        event to happen.

        The delay is scaled according to the real-time :attr:`factor`. With
        :attr:`strict` mode enabled, a :exc:`RuntimeError` will be raised, if
        the event is processed too slowly.

        """
        evt_time = self.peek()

        if evt_time is Infinity:
            raise EmptySchedule()

        real_time = self.real_start + (evt_time - self.env_start) * self.factor

        if self.strict and monotonic() - real_time > self.factor:
            # Events scheduled for time *t* may take just up to *t+1*
            # for their computation, before an error is raised.
            delta = monotonic() - real_time
            raise RuntimeError(
                f'Simulation too slow for real time ({delta:.3f}s).'
            )

        # Sleep in a loop to fix inaccuracies of windows (see
        # https://stackoverflow.com/a/15967564 for details) and to ignore
        # interrupts.
        while True:
            delta = real_time - monotonic()
            if delta <= 0:
                break
            await asyncio.sleep(delta)

        Environment.step(self)

    async def run(
        self, until: Optional[Union[SimTime, Event]] = None
    ) -> Optional[Any]:
        """Executes :meth:`step()` until the given criterion *until* is met.

        - If it is ``None`` (which is the default), this method will return
          when there are no further events to be processed.

        - If it is an :class:`~simpy.events.Event`, the method will continue
          stepping until this event has been triggered and will return its
          value.  Raises a :exc:`RuntimeError` if there are no further events
          to be processed and the *until* event was not triggered.

        - If it is a number, the method will continue stepping
          until the environment's time reaches *until*.

        """
        if until is not None:
            if not isinstance(until, Event):
                # Assume that *until* is a number if it is not None and
                # not an event.  Create a Timeout(until) in this case.
                at: SimTime
                if isinstance(until, int):
                    at = until
                else:
                    at = float(until)

                if at <= self.now:
                    raise ValueError(
                        f'until(={at}) must be > the current simulation time.'
                    )

                # Schedule the event before all regular timeouts.
                until = Event(self)
                until._ok = True
                until._value = None
                self.schedule(until, URGENT, at - self.now)

            elif until.callbacks is None:
                # Until event has already been processed.
                return until.value

            until.callbacks.append(StopSimulation.callback)

        try:
            while True:
                await self.step()
        except StopSimulation as exc:
            return exc.args[0]  # == until.value
        except EmptySchedule as e:
            if until is not None:
                assert not until.triggered
                raise RuntimeError(
                    f'No scheduled events left but "until" event was not '
                    f'triggered: {until}'
                ) from e
        return None
