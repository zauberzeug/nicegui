#!/usr/bin/env python3
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from nicegui import ui

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_):
    worker_id = os.getpid()
    logging.info(f'Worker {worker_id} started')
    yield


@ui.page('/')
def show():
    logging.info(f'Handling request in worker {os.getpid()}')
    ui.label('Hello, FastAPI!')


app = FastAPI(lifespan=lifespan)
ui.run_with(app)

if __name__ == '__main__':
    print('Please start the app with a "uvicorn" command as shown in the start.sh script')
