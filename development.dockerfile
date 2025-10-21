FROM python:3.9-slim

RUN apt update && apt install curl build-essential -y

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY . .
RUN uv sync --all-extras

RUN pip install latex2mathml

CMD python3 -m debugpy --listen 5678 main.py
