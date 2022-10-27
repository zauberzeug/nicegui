FROM python:3.11-slim

RUN python -m pip install nicegui

WORKDIR /app

COPY main.py traffic_tracking.py api_docs_and_examples.py README.md ./ 
ADD examples ./examples

EXPOSE 80

CMD python3 main.py
