#!/usr/bin/env python3
import justpy as jp
import inspect
import uvicorn
import asyncio

wp = jp.WebPage(delete_flag=False, head_html='<script>confirm = () => true;</script>')

main = jp.Div(a=wp, text='This minimal test is working nicely. "LOOP" is printed every second.')
main.add_page(wp)
jp.justpy(lambda: wp, start_server=False)
app = jp.app

async def loop():
    while True:
        print('LOOP')
        await asyncio.sleep(1.0)
jp.run_task(loop())

def run():
    if not inspect.stack()[-2].filename.endswith('spawn.py'):
        uvicorn.run('test:app', host='0.0.0.0', port=80, lifespan='on', reload=True)
run()
