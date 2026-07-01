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

**Event payloads are encrypted by default.** Each payload is sealed with a Fernet key (AES-128-CBC + HMAC-SHA256) derived from your `storage_secret` via HKDF before it goes on the wire, and opened on receipt. The secret never crosses the wire, so a node that doesn't share it sees only ciphertext and cannot forge a valid event — undecryptable messages (foreign deployment, forged, or older than `EVENT_TTL_SECONDS`) are dropped silently. This gives you **confidentiality and integrity of event data** even on a shared network.

The `storage_secret`-derived **topic namespace is collision-avoidance only** — it stops unrelated deployments from accidentally sharing topics, but is **not** a security boundary: the derived prefix travels in Zenoh declarations/interests, so any node on the network can observe it.

**Residuals to keep in mind for an internet-exposed deployment:**

- **Metadata still leaks** — topic / key-expression names, message timing, and payload sizes are visible to any node on the network (only the payload bytes are encrypted).
- **Denial-of-service** (flooding the network or a topic) is not prevented by encryption.

For defense-in-depth on a shared or untrusted network, also secure the Zenoh transport itself — pass a raw Zenoh config dict to `distributed=` with **mTLS** node authentication ([zenoh.io/docs/manual/tls](https://zenoh.io/docs/manual/tls/)) and an **`access_control`** ACL (`default_permission: deny`) that allows pub/sub only for authenticated subjects ([zenoh.io/docs/manual/access-control](https://zenoh.io/docs/manual/access-control/)) — or keep the Zenoh transport on a network you control.
