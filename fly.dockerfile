FROM python:3.11-slim

LABEL maintainer="Zauberzeug GmbH <info@zauberzeug.com>"

WORKDIR /app

ADD . .
RUN pip install -e .
RUN pip install itsdangerous prometheus_client

EXPOSE 8080
EXPOSE 9062

CMD python3 main.py
