#!/usr/bin/env python3
import asyncio
import datetime

from async_realtime_environment import AsyncRealtimeEnvironment

from nicegui import ui

start_time = datetime.datetime.now()


def clock(env):
    while True:
        simulation_time = start_time + datetime.timedelta(seconds=env.now)
        clock_label.text = simulation_time.strftime('%H:%M:%S')
        yield env.timeout(1)


def traffic_light(env):
    while True:
        light.classes('bg-green-500', remove='bg-red-500')
        yield env.timeout(30)
        light.classes('bg-yellow-500', remove='bg-green-500')
        yield env.timeout(5)
        light.classes('bg-red-500', remove='bg-yellow-500')
        yield env.timeout(20)


async def run_simpy():
    env = AsyncRealtimeEnvironment(factor=0.1)  # fast forward simulation with 1/10th of realtime
    env.process(traffic_light(env))
    env.process(clock(env))
    try:
        await env.run(until=300)  # run until 300 seconds of simulation time have passed
    except asyncio.CancelledError:
        return
    ui.notify('Simulation completed')
    content.classes('opacity-0')  # fade out the content

# define the UI
with ui.column().classes('absolute-center items-center transition-opacity duration-500') as content:
    ui.label('SimPy Traffic Light Demo').classes('text-2xl mb-6')
    light = ui.element('div').classes('w-10 h-10 rounded-full shadow-lg transition')
    clock_label = ui.label()

# start the simpy simulation as an async task in the background as soon as the UI is ready
ui.timer(0, run_simpy, once=True)

ui.run()
