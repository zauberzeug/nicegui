FROM python:3.8-slim as builder

RUN apt update && apt install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip

# netifaces needs to be compiled on some platforms (macos ARM for example)
RUN python3 -m pip install netifaces

FROM python:3.8-slim as devcontainer

ENV POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:99

# Chrome and chromedriver versions must match
# See https://chromiumdash.appspot.com/home
ARG CHROMIUM_VERSION=117.0.5938.62

# Create remote user and install google chromium and chromium-driver
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update && apt-get install --no-install-recommends -y \
    sudo git chromium=${CHROMIUM_VERSION}* chromium-driver=${CHROMIUM_VERSION}* \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

# Install nicegui
RUN pip install -U pip && pip install poetry==$POETRY_VERSION
COPY nicegui pyproject.toml poetry.lock README.md ./
RUN poetry install --all-extras

WORKDIR /workspaces/nicegui
USER $USERNAME

ENTRYPOINT ["poetry", "run", "python", "-m", "debugpy", "--listen" ,"5678", "main.py"]