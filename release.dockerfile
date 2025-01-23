FROM python:3.11-slim AS builder

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN python -m pip install --upgrade pip

RUN python -m pip install --upgrade libsass

FROM python:3.11-slim AS release
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
ARG VERSION

LABEL maintainer="Zauberzeug GmbH <info@zauberzeug.com>"

RUN python -m pip install --upgrade pip

RUN python -m pip install \
    nicegui[plotly,matplotlib]==$VERSION \
    docutils \
    isort \
    itsdangerous \
    pytest \
    requests \
    latex2mathml \
    selenium \
    redis

WORKDIR /app

COPY main.py README.md prometheus.py ./
COPY examples ./examples
COPY website ./website
RUN mkdir /resources
COPY docker-entrypoint.sh /resources
RUN chmod 777 /resources/docker-entrypoint.sh

EXPOSE 8080
ENV PYTHONUNBUFFERED=True

ENTRYPOINT ["/resources/docker-entrypoint.sh"]
CMD ["python", "main.py"]
