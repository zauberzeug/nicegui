#!/usr/bin/env python
import icecream

from nicegui import APIRouter, app, ui

icecream.install()

router = APIRouter(prefix='/router')
app.include_router(router)
ui.link('go to router', '/router')
ui.link('go to subpage', '/subpage')


@router.page('/')
def router_page():
    ui.label('Hello from APIRouter!')


@ui.page('/subpage')
def subpage():
    ui.label('Hello from subpage!')


ui.run(on_air='oazK7cSg3eG6n105', port=2391)
