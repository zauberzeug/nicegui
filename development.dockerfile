FROM python:3.9-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

ARG VERSION="0.0.0"
ENV POETRY_DYNAMIC_VERSIONING_BYPASS=$VERSION

COPY . .
RUN uv sync

CMD ["uv", "run", "python3", "-m", "debugpy", "--listen", "5678", "main.py"]
