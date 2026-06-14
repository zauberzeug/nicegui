# Distributed Events

`DistributedEvent` instances are automatically shared across all NiceGUI instances when you enable distributed mode (`ui.run(distributed=True)`).

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

## Security / trust model

Distributed mode assumes a **trusted Zenoh network**. The `storage_secret`-derived topic namespace is **collision-avoidance only** — it stops unrelated deployments from accidentally sharing topics, but it is **not** a confidentiality boundary: the derived prefix travels in Zenoh declarations/interests, so any node on the same network can observe it and subscribe. The secret itself never crosses the wire.

For real isolation on a shared or untrusted network, secure the transport rather than relying on the namespace — pass a raw Zenoh config dict to `distributed=` with:

- **mTLS** node authentication ([zenoh.io/docs/manual/tls](https://zenoh.io/docs/manual/tls/)), and
- an **`access_control`** ACL to allow/deny pub/sub by key-expression and authenticated subject ([zenoh.io/docs/manual/access-control](https://zenoh.io/docs/manual/access-control/)).

End-to-end payload secrecy would additionally need message-level security (e.g. the experimental [zenoh-mls](https://codeberg.org/permian/zenoh-mls)).
