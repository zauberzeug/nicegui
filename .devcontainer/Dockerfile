FROM --platform=linux/amd64 python:3.8

ENV POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_VIRTUALENVS_CREATE=false \
    DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:99

# Install packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git build-essential chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Create remote user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
ENV CHROME_BINARY_LOCATION=/usr/bin/chromium

# Install nicegui
RUN pip install -U pip && pip install poetry==$POETRY_VERSION
COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --all-extras --no-root
RUN pip install latex2mathml

USER $USERNAME

ENTRYPOINT ["poetry", "run", "python", "-m", "debugpy", "--listen" ,"5678", "main.py"]
