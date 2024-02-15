#!/usr/bin/env python3
import frontend
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    """
    Returns a dictionary with a simple 'Hello' message.

    This function is used as a FastAPI endpoint to handle the root route.
    It returns a dictionary with a key 'Hello' and value 'World'.

    Returns:
        dict: A dictionary with a 'Hello' message.

    Example:
        >>> read_root()
        {'Hello': 'World'}
    """
    return {'Hello': 'World'}


frontend.init(app)

if __name__ == '__main__':
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')
