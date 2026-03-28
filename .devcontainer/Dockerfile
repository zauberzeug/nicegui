FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:99

# Install packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git chromium chromium-driver gh \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

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
COPY pyproject.toml uv.lock* README.md ./
RUN uv sync --no-install-project --all-extras

USER $USERNAME

ENTRYPOINT ["uv", "run", "python", "-m", "debugpy", "--listen" ,"5678", "main.py"]
