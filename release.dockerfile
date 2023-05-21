FROM python:3.11.3-slim
ARG VERSION

LABEL maintainer="Zauberzeug GmbH <info@zauberzeug.com>"

RUN python -m pip install nicegui==$VERSION itsdangerous isort docutils

WORKDIR /app

COPY main.py README.md prometheus.py ./ 
ADD examples ./examples
ADD website ./website

EXPOSE 8080

CMD python3 main.py
