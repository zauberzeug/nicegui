FROM python:3.12-slim

LABEL maintainer="Zauberzeug GmbH <info@zauberzeug.com>"

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock* ./

# Install dependencies including website group
ARG VERSION
ENV POETRY_DYNAMIC_VERSIONING_BYPASS=$VERSION
RUN uv sync --no-install-project --no-dev --all-extras --group website

# Copy application files
COPY main.py README.md ./
COPY examples ./examples
COPY website ./website
RUN mkdir /resources
COPY docker-entrypoint.sh /resources
RUN chmod 777 /resources/docker-entrypoint.sh

# Install NiceGUI from source
RUN uv pip install .

EXPOSE 8080
ENV PYTHONUNBUFFERED=True

ENTRYPOINT ["/resources/docker-entrypoint.sh"]
CMD ["python", "main.py"]
