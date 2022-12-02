#!/usr/bin/env python3
import frontend
from fastapi import FastAPI

app = FastAPI()
frontend.init(app)


@app.get('/')
def read_root():
    return {'Hello': 'World'}
