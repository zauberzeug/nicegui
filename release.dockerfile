ARG VERSION
FROM python:3.11-slim

LABEL maintainer="Zauberzeug GmbH <info@zauberzeug.com>"

RUN python -m pip install nicegui==$VERSION

WORKDIR /app

COPY main.py traffic_tracking.py api_docs_and_examples.py README.md ./ 
ADD examples ./examples

EXPOSE 8080

CMD python3 main.py
