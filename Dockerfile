FROM python:3.7.16 as base

ENV POETRY_VERSION=1.4.0 \
    PATH="/root/.local/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_INSTALLER_MAX_WORKERS=10

RUN curl -sSL https://install.python-poetry.org | python - && \
    poetry completions bash >> ~/.bash_completion

COPY pyproject.toml poetry.lock /

RUN poetry install --without=dev --no-root

FROM base as chromium-driver

RUN apt-get update -y && \
    apt-get install -y xvfb wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


ENV CHROME_BIN=/usr/bin/google-chrome \
    CHROME_PATH=/usr/bin/google-chrome \
    CHROMEDRIVER_PATH=/usr/local/bin/chromedriver \
    DISPLAY=:99

FROM chromium-driver as development

ENV ENVIRONMENT=DEVELOPMENT 

RUN poetry install --no-root

FROM chromium-driver as testing

ENV ENVIRONMENT=TESTING

ADD /nicegui /nicegui
ADD /tests /tests

CMD pytest -p no:cov --junitxml /temp/result.xml -n $(nproc) /tests
