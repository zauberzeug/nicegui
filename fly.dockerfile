FROM python:3.11-slim

LABEL maintainer="Zauberzeug GmbH <nicegui@zauberzeug.com>"

RUN apt update && apt install -y curl procps

RUN pip install \
    dnspython \
    docutils \
    isort \
    itsdangerous \
    matplotlib \
    pandas \
    plotly \
    prometheus_client \
    pyecharts \
    pytest \
    requests \
    selenium

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && \
    ln -s ~/.local/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock*  ./

RUN poetry install --no-root --extras "plotly matplotlib highcharts sass"

RUN pip install latex2mathml

ADD . .

# ensure unique version to not serve cached and hence potentially wrong static files
ARG VERSION=unknown
RUN if [ "$VERSION" = "unknown" ]; then echo "Error: VERSION build argument is required. Use: fly deploy --build-arg VERSION=$(git describe --abbrev=0 --tags --match 'v*' 2>/dev/null | sed 's/^v//' || echo '0.0.0')" && exit 1; fi
RUN sed -i "/\[tool.poetry\]/,/]/s/version = .*/version = \"$VERSION\"/" pyproject.toml

RUN pip install .

EXPOSE 8080
EXPOSE 9062

COPY fly-entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
