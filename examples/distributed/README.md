# Distributed Events

Events are automatically shared across all NiceGUI instances when you enable distributed mode.

## Quick Start

```bash
pip install "nicegui[distributed]"
python main.py
```

Run on multiple machines/terminals to see events propagate.

## Docker Swarm Demo

```bash
docker swarm init
docker stack deploy -c docker-compose.yml distributed
```

Open http://localhost:8080 in multiple browser tabs/windows.

Update:

```bash
docker stack deploy -c docker-compose.yml distributed
```

Clean up:

```bash
docker stack rm distributed
docker swarm leave --force
```
