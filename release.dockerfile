FROM python:3.10-slim

RUN apt update && apt install -y \
    python3-numpy \ 
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install nicegui

WORKDIR /app

COPY main.py README.md ./ 

EXPOSE 80

CMD python3 main.py
