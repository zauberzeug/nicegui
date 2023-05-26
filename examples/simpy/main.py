#!/usr/bin/env python3
import datetime

from async_realtime_environment import AsyncRealtimeEnvironment

from nicegui import ui

start_time = datetime.datetime.now()


def clock(env):
    while True:
        simulation_time = start_time + datetime.timedelta(seconds=env.now)
        clock_label.set_text(simulation_time.strftime('%H:%M:%S'))
        yield env.timeout(1)


def traffic_light(env):
    while True:
        lblColor.set_text('GREEN')
        yield env.timeout(30)
        lblColor.set_text('YELLOW')
        yield env.timeout(5)
        lblColor.set_text('RED')
        yield env.timeout(20)


async def run_simpy():
    env = AsyncRealtimeEnvironment(factor=0.1)  # fast forward simulation with 1/10th of realtime
    env.process(traffic_light(env))
    env.process(clock(env))
    await env.run(until=300)  # run until 300 seconds of simulation time have passed
    ui.notify('Simulation completed')

# create the UI
clock_label = ui.label()
lblColor = ui.label()

# start the simpy simulation as async task in the background as soon as the UI is ready
ui.timer(0, run_simpy, once=True)
ui.run()
