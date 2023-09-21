FROM python:3.8-slim as base

ENV POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_VIRTUALENVS_CREATE=false \
    DEBIAN_FRONTEND=noninteractive \
    SHELL=/bin/bash \
    DISPLAY=:99

FROM base as builder

RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Netifaces needs to be compiled on some platforms (macos ARM for example)
RUN pip install -U pip && pip install netifaces

FROM base as devcontainer

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

# Install packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Create remote user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install nicegui
RUN pip install -U pip && pip install poetry==$POETRY_VERSION
COPY nicegui pyproject.toml poetry.lock README.md ./
RUN poetry install --all-extras

WORKDIR /workspaces/nicegui
USER $USERNAME

ENTRYPOINT ["poetry", "run", "python", "-m", "debugpy", "--listen" ,"5678", "main.py"]