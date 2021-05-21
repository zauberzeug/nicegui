FROM python:3.9-slim

RUN python -m pip install nicegui

WORKDIR /app

COPY main.py README.md . 

EXPOSE 80

CMD python3 main.py
