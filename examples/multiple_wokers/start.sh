#!/usr/bin/env bash

cd "$(dirname "$0")" # use path of this example as working directory; enables starting this script from anywhere
uvicorn main:app --log-level warning --workers 4 --port 8000
