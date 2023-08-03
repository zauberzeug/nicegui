#!/usr/bin/env python3
from datetime import datetime

from nicegui import ui


def build_svg() -> str:
    """Returns an SVG showing the current time.

        Original was borrowed from https://de.m.wikipedia.org/wiki/Datei:Station_Clock.svg.
    """
    now = datetime.now()
    return f'''
        <svg width="800" height="800" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <circle cx="400" cy="400" r="400" fill="#fff"/>
            <use transform="matrix(-1,0,0,1,800,0)" xlink:href="#c"/>
            <g id="c">
                <g id="d">
                    <path d="m400 40v107" stroke="#000" stroke-width="26.7"/>
                    <g id="a">
                        <path d="m580 88.233-42.5 73.612" stroke="#000" stroke-width="26.7"/>
                        <g id="e">
                            <path id="b" d="m437.63 41.974-3.6585 34.808" stroke="#000" stroke-width="13.6"/>
                            <use transform="rotate(6 400 400)" xlink:href="#b"/>
                        </g>
                        <use transform="rotate(12 400 400)" xlink:href="#e"/>
                    </g>
                    <use transform="rotate(30 400 400)" xlink:href="#a"/>
                    <use transform="rotate(60 400 400)" xlink:href="#a"/>
                </g>
                <use transform="rotate(90 400 400)" xlink:href="#d"/>
            </g>
            <g transform="rotate({250 + now.hour / 12 * 360} 400 400)">
                <path d="m334.31 357.65-12.068 33.669 283.94 100.8 23.565-10.394-13.332-24.325z"/>
            </g>
            <g transform="rotate({117 + now.minute / 60 * 360} 400 400)">
                <path d="m480.73 344.98 11.019 21.459-382.37 199.37-18.243-7.2122 4.768-19.029z"/>
            </g>
            <g transform="rotate({169 + now.second / 60 * 360} 400 400)">
                <path d="m410.21 301.98-43.314 242.68a41.963 41.963 0 0 0-2.8605-0.091 41.963 41.963 0 0 0-41.865 42.059 41.963 41.963 0 0 0 30.073 40.144l-18.417 103.18 1.9709 3.9629 3.2997-2.9496 21.156-102.65a41.963 41.963 0 0 0 3.9771 0.1799 41.963 41.963 0 0 0 41.865-42.059 41.963 41.963 0 0 0-29.003-39.815l49.762-241.44zm-42.448 265.56a19.336 19.336 0 0 1 15.703 18.948 19.336 19.336 0 0 1-19.291 19.38 19.336 19.336 0 0 1-19.38-19.291 19.336 19.336 0 0 1 19.291-19.38 19.336 19.336 0 0 1 3.6752 0.3426z" fill="#a40000"/>
            </g>
        </svg>
    '''


clock = ui.html().classes('self-center')
ui.timer(1, lambda: clock.set_content(build_svg()))

ui.run()
