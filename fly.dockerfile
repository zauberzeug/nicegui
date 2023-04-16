FROM python:3.11-slim

LABEL maintainer="Zauberzeug GmbH <nicegui@zauberzeug.com>"

RUN pip install itsdangerous prometheus_client isort docutils

WORKDIR /app

ADD . .

# ensure unique version to not serve cached and hence potentially wrong static files
ARG VERSION=unknown
RUN if [ "$VERSION" = "unknown" ]; then echo "Error: VERSION build argument is required. Use: fly deploy --build-arg VERSION=$(git describe --abbrev=0 --tags --match 'v*' 2>/dev/null || echo 'v0.0.0')" && exit 1; fi
RUN sed -i "/\[tool.poetry\]/,/]/s/version = .*/version = \"$VERSION\"/" pyproject.toml

RUN cat pyproject.toml
RUN pip install .

# EXPOSE 8080
# EXPOSE 9062

# CMD python3 main.py
