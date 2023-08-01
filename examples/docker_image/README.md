# Docker Example

This example shows how to use the NiceGUI release docker image
[zauberzeug/nicegui from Docker Hub](https://hub.docker.com/r/zauberzeug/nicegui).
It uses a `docker-compose.yml` file for convenience.
Similar behavior can be archived with `docker run` and the corresponding parameters.

## Try it out.

Alter the docker-compose.yml file to your local host user's uid/gid and then run

```bash
docker compose up
```

## Special Docker Features

### Storage

NiceGUI automatically creates a `.nicegui` directory in the applications root directory (`/app` inside the docker container).
In this example we mount the local `app` folder into the `/app` location of the container.
This makes the `.nicegui` folder persistent across docker restarts.
You can access http://localhost:8080, enter some data for storage and verify by restarting the container.

### Non-Root User

The app inside the container is executed as non-root.
All files created by NiceGUI (for example the `.nicegui` persistence) will have the configured uid/gid.

### Docker signals

The docker image will passe signals from Docker like SIGTERM to issue a graceful shutdown of NiceGUI.
If you stop the container (eg. Ctrl+C) and look at the logs (`docker compose logs) you should see it initiated `ui.shutdown` method.
