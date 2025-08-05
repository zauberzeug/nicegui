FROM python:3.9-slim

RUN apt update && apt install curl build-essential -y

RUN python -m pip install --no-cache-dir "poetry~=1.8" \
    && poetry config virtualenvs.create false

WORKDIR /app

COPY . .
RUN poetry install --all-extras

RUN pip install latex2mathml

CMD python3 -m debugpy --listen 5678 main.py
