FROM python:3.8-slim

# Chrome and chromedriver versions must match as per
# https://googlechromelabs.github.io/chrome-for-testing/#stable
ARG CHROME_VERSION=116.0.5845.96

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV POETRY_VERSION=1.6.1 \
    PATH="/home/$USERNAME/.local/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    DISPLAY=:99

# Create remote user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo git wget gnupg unzip curl \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

# Install google chrome
RUN wget -nv -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb \
    && apt-get update && apt-get install -y /tmp/chrome.deb \
    && rm /tmp/chrome.deb

# Install chromedriver to a PATH directory
RUN wget -nv -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip \
    && unzip -j /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

USER $USERNAME
WORKDIR /workspaces/nicegui

RUN pip install -U pip && pip install poetry==$POETRY_VERSION

COPY ./pyproject.toml ./poetry.lock* main.py ./
RUN poetry install --all-extras

CMD python -m debugpy --listen 5678 main.py