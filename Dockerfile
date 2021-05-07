FROM python:3.9-slim

RUN apt update && apt install openssh-server sudo vim less ack-grep rsync wget curl bash -y && rm -rf /var/lib/apt/lists/*

# We use Poetry for dependency management
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* main.py ./
RUN poetry install --no-root

# do not show reload warning popup (see https://github.com/elimintz/justpy/issues/236#issuecomment-799431208)
RUN sed -i "s/confirm('Page needs to be reloaded, click OK to reload')/true/g" /usr/local/lib/python3.9/site-packages/justpy/templates/main.html

CMD uvicorn --reload --host 0.0.0.0 --port 80 main:app