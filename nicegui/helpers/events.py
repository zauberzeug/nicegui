import asyncio


def link_events(source: asyncio.Event, target: asyncio.Event) -> asyncio.Task:
    """Make one event fires the other."""
    async def _forward():
        await source.wait()
        target.set()
    return asyncio.create_task(_forward())
