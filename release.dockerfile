FROM python:3.10-slim

RUN python -m pip install nicegui

WORKDIR /app

COPY main.py traffic_tracking.py README.md ./ 

EXPOSE 80

CMD python3 main.py
