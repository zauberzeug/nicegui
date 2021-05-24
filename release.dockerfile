FROM python:3.9-slim

RUN python -m pip install nicegui

RUN apt update && apt install patch -y && rm -rf /var/lib/apt/lists/*
WORKDIR /usr/local/lib/python3.9/site-packages/justpy/
COPY justpy_allow-hosting-behind-reverse-proxy-with-prefixed-path.patch .
RUN patch -p1 < justpy_allow-hosting-behind-reverse-proxy-with-prefixed-path.patch

WORKDIR /app

COPY main.py README.md . 

EXPOSE 80

CMD python3 main.py
