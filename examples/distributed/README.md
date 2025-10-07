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

Clean up:

```bash
docker stack rm distributed
docker swarm leave --force
```

## How it Works

- Click emoji → `reaction_event.emit(emoji)` fires
- Event propagates via Zenoh P2P to all instances
- Each instance runs the animation independently
- Events are ephemeral - no storage, just pure messaging!

API:

- `Event()` - distributed across all instances
- `Event(local=True)` - stays on current instance
- `ui.run(distributed=True)` - enables distributed mode
