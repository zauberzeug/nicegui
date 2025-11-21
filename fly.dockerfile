FROM python:3.12-slim

LABEL maintainer="Zauberzeug GmbH <nicegui@zauberzeug.com>"

RUN apt update && apt install -y curl procps build-essential
RUN pip install --upgrade pip

RUN pip install \
    dnspython \
    docutils \
    httpx \
    isort \
    itsdangerous \
    matplotlib \
    pandas \
    plotly \
    pyecharts \
    pytest \
    selenium

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --no-dev --extra plotly --extra matplotlib --extra highcharts

RUN pip install latex2mathml slowapi

ADD . .

# ensure unique version to not serve cached and hence potentially wrong static files
ARG VERSION=unknown
RUN if [ "$VERSION" = "unknown" ]; then echo "Error: VERSION build argument is required. Use: fly deploy --build-arg VERSION=$(git describe --abbrev=0 --tags --match 'v*' 2>/dev/null | sed 's/^v//' || echo '0.0.0')" && exit 1; fi
RUN sed -i "/^\[project\]/,/^version = /s/version = .*/version = \"$VERSION\"/" pyproject.toml

ENV POETRY_DYNAMIC_VERSIONING_BYPASS=$VERSION
RUN uv pip install --system .

EXPOSE 8080

COPY fly-entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

ENV PYTHONUNBUFFERED=1
ENV ENABLE_ANALYTICS=true

CMD ["python", "main.py"]
