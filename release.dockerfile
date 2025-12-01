FROM python:3.12-slim

LABEL maintainer="Zauberzeug GmbH <info@zauberzeug.com>"

RUN python -m pip install --upgrade pip

ARG VERSION
# isort is needed for the documentation
RUN python -m pip install nicegui[native,plotly,matplotlib,highcharts,redis]==$VERSION \
    isort \
    pytest \
    latex2mathml \
    selenium \
    pytest-selenium

WORKDIR /app

COPY main.py README.md ./
COPY examples ./examples
COPY website ./website
RUN mkdir /resources
COPY docker-entrypoint.sh /resources
RUN chmod 777 /resources/docker-entrypoint.sh

EXPOSE 8080
ENV PYTHONUNBUFFERED=True

ENTRYPOINT ["/resources/docker-entrypoint.sh"]
CMD ["python", "main.py"]
