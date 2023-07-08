FROM python:3.8-slim

RUN apt update && apt install curl -y

# We use Poetry for dependency management
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && \
    ln -s ~/.local/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* main.py ./
RUN poetry install --no-root --all-extras

CMD python3 -m debugpy --listen 5678 main.py
