FROM python:3.8-slim

RUN apt update && apt install curl build-essential -y

# The next few lines are the original command commented out
# but kept in the file to quickly swap back once development.dockerfile
# is upgraded to use python 3.11.


# We use Poetry for dependency management
#RUN curl -sSL https://install.python-poetry.org | python3 - && \
#    cd /usr/local/bin && \
#    ln -s ~/.local/bin/poetry && \
#    poetry config virtualenvs.create fals

# pin the last seed packages that still support 3.8
RUN python -m pip install --upgrade "pip<25" "setuptools<80" wheel
RUN python -m pip install "virtualenv<20.31" "poetry==1.8.5" && poetry config virtualenvs.create false

WORKDIR /app

COPY . .
RUN poetry install --all-extras

RUN pip install latex2mathml

CMD python3 -m debugpy --listen 5678 main.py
