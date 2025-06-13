# Using Redis for session storage

NiceGUI can use Redis for storage. To make this work, you set environment variables:

## `NICEGUI_REDIS_URL`

This is the only required variable. Setting it to a full Redis server connection string will make NiceGUI switch to Redis for storage

## `NICEGUI_REDIS_PREFIX`

The prefix that will be used on the Redis server for the values set from the NiceGUI server. Default is `nicegui:`. If you have two environments using the same Redis server/cluster, use this prefix to separate them.

## Control how NiceGUI establishes the Redis connection

When NiceGUI starts, and the `NICEGUI_REDIS_URL` is set, it will establish the connection. Sometimes you want to control the arguments for this connection (you can read more on the Python Redis package documentation). The following are defined as environment variables:

- `NICEGUI_REDIS_HEALTH_CHECK_INTERVAL` (default: 10) as connection argument `health_check_interval`
- `NICEGUI_REDIS_SOCKET_CONNECT_TIMEOUT` (default: 5) as connection argument `socket_connect_timeout`
- `NICEGUI_REDIS_RETRY_ON_TIMEOUT` (default: True) as connection argument `retry_on_timeout`
- `NICEGUI_REDIS_SOCKET_KEEPALIVE` (default: True) sa connection argument `socket_keepalive`

All environment values are always strings. The boolean values needed for the two last settings will be interpreted from 0/1 or true/false.
