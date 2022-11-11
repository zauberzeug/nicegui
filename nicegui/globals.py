import asyncio
import logging
from typing import TYPE_CHECKING, Dict, List, Optional

from fastapi import FastAPI
from socketio import AsyncServer

if TYPE_CHECKING:
    from .client import Client

app: FastAPI
sio: AsyncServer
loop: Optional[asyncio.AbstractEventLoop] = None
log: logging.Logger = logging.getLogger('nicegui')

client_stack: List['Client'] = []
clients: Dict[int, 'Client'] = {}
next_client_id: int = 0
