#!/usr/bin/env python3
import threading
from datetime import datetime

from async_realtime_environment import AsyncRealtimeEnvironment

from nicegui import app, ui

lblTick = ui.label()
lblColor = ui.label()


def clock(env):
    while True:
        lblTick.set_text(datetime.now().strftime("%H:%M:%S"))
        # lblTick.set_text(f"{env.now}")
        yield env.timeout(1)


def traffic_light(env):
    while True:
        lblColor.set_text("GREEN")
        yield env.timeout(30)
        lblColor.set_text("YELLOW")
        yield env.timeout(5)
        lblColor.set_text("RED")
        yield env.timeout(20)


async def run_simpy():
    env = AsyncRealtimeEnvironment(factor=0.1)
    env.process(traffic_light(env))
    env.process(clock(env))
    await env.run(until=300)
    print("Simulation complete")


ui.timer(0, run_simpy, once=True)
ui.run()
