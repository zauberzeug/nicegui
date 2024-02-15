#!/usr/bin/env python3
import asyncio
import datetime

from async_realtime_environment import AsyncRealtimeEnvironment

from nicegui import ui

start_time = datetime.datetime.now()


def clock(env):
    """
    A clock generator for simulating time in a simulation environment.

    Parameters:
    - env (simpy.Environment): The simulation environment.

    Yields:
    - simpy.Timeout: A timeout event that represents the passage of time.

    Usage:
    1. Create a simulation environment using simpy.Environment().
    2. Pass the simulation environment to the clock() function.
    3. Use the yielded timeout event to advance the simulation time.

    Example:
    env = simpy.Environment()
    env.process(clock(env))
    env.run(until=10)  # Run the simulation for 10 time units.
    """
    while True:
        simulation_time = start_time + datetime.timedelta(seconds=env.now)
        clock_label.text = simulation_time.strftime('%H:%M:%S')
        yield env.timeout(1)


def traffic_light(env):
    """
    Simulates a traffic light using a generator function.

    The traffic light cycles through three states: green, yellow, and red.
    It uses the `env.timeout()` function from the SimPy library to introduce delays between state changes.

    Parameters:
    - env (simpy.Environment): The SimPy environment in which the traffic light is being simulated.

    Yields:
    - simpy.Timeout: A timeout event that represents the delay between state changes.

    Usage:
    1. Create a SimPy environment: `env = simpy.Environment()`
    2. Create a traffic light process: `env.process(traffic_light(env))`
    3. Run the simulation: `env.run(until=100)`
    """
    while True:
        light.classes('bg-green-500', remove='bg-red-500')
        yield env.timeout(30)
        light.classes('bg-yellow-500', remove='bg-green-500')
        yield env.timeout(5)
        light.classes('bg-red-500', remove='bg-yellow-500')
        yield env.timeout(20)


async def run_simpy():
    """
    Run a simulation using SimPy.

    This function sets up the simulation environment, processes, and runs the simulation until a specified time.
    It uses an AsyncRealtimeEnvironment with a fast forward factor of 0.1, which means the simulation runs at 1/10th of real-time speed.
    The simulation includes a traffic_light process and a clock process.

    Parameters:
        None

    Returns:
        None

    Raises:
        asyncio.CancelledError: If the simulation is cancelled.

    Usage:
        - Import the run_simpy function from this module.
        - Call the run_simpy function to start the simulation.
        - The simulation will run until 300 seconds of simulation time have passed.
        - If the simulation is cancelled, the function will return without raising an exception.
        - After the simulation completes, a notification will be displayed and the content will fade out.

    Example:
        await run_simpy()
    """
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
