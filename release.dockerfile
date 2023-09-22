FROM python:3.11.3-slim
ARG VERSION

LABEL maintainer="Zauberzeug GmbH <info@zauberzeug.com>"

RUN python -m pip install nicegui==$VERSION itsdangerous isort docutils requests

WORKDIR /app

COPY main.py README.md prometheus.py ./
COPY examples ./examples
COPY website ./website
RUN mkdir /resources
COPY docker-entrypoint.sh /resources
RUN chmod 777 /resources/docker-entrypoint.sh

EXPOSE 8080
ENV PYTHONUNBUFFERED True
ENV NO_NETIFACES=true

ENTRYPOINT ["/resources/docker-entrypoint.sh"]
CMD ["python", "main.py"]