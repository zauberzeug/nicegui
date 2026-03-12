#!/usr/bin/env python3
import asyncio
import datetime

from async_realtime_environment import AsyncRealtimeEnvironment

from nicegui import Event, ui

start_time = datetime.datetime.now()


time_updated = Event()
light_updated = Event()
simulation_completed = Event()


def clock(env):
    while True:
        simulation_time = start_time + datetime.timedelta(seconds=env.now)
        time_updated.emit(simulation_time.strftime('%H:%M:%S'))
        yield env.timeout(1)


def traffic_light(env):
    while True:
        light_updated.emit('green')
        yield env.timeout(30)
        light_updated.emit('yellow')
        yield env.timeout(5)
        light_updated.emit('red')
        yield env.timeout(20)


async def run_simpy():
    env = AsyncRealtimeEnvironment(factor=0.1)  # fast forward simulation with 1/10th of realtime
    env.process(traffic_light(env))
    env.process(clock(env))
    try:
        await env.run(until=300)  # run until 300 seconds of simulation time have passed
    except asyncio.CancelledError:
        return
    simulation_completed.emit()


@ui.page('/')
def page():
    # define the UI
    with ui.column().classes('absolute-center items-center transition-opacity duration-500'):
        ui.label('SimPy Traffic Light Demo').classes('text-2xl mb-6')
        light = ui.element('div').classes('w-10 h-10 rounded-full shadow-lg transition')
        clock_label = ui.label()

        time_updated.subscribe(clock_label.set_text)
        light_updated.subscribe(lambda color: light.classes(f'bg-{color}-500',
                                                            remove='bg-red-500 bg-green-500 bg-yellow-500'))
        simulation_completed.subscribe(lambda: ui.notify('Simulation completed'))

        ui.button('Run Simulation') \
            .on_click(run_simpy) \
            .on_click(lambda e: e.sender.delete())


ui.run()
