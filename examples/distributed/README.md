# Distributed Events

Events are automatically shared across all NiceGUI instances when you enable distributed mode (`ui.run(distributed=True)`).

## Demo

This demo uses docker swarm to deploy multiple NiceGUI instances with a Traefik load balancer in front.

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
