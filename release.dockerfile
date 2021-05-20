FROM python:3.9-slim

RUN python -m pip install 'nicegui>=0.2.4'

WORKDIR /app

COPY main.py README.md . 

CMD python3 main.py
