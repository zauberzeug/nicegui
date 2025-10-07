FROM python:3.11-slim

WORKDIR /app

# Copy and install NiceGUI with distributed support
COPY nicegui /tmp/nicegui/nicegui
COPY pyproject.toml LICENSE README.md /tmp/nicegui/
RUN pip install --no-cache-dir /tmp/nicegui[distributed] && rm -rf /tmp/nicegui

# main.py will be mounted for hot reload

EXPOSE 8080

CMD ["python", "main.py"]
