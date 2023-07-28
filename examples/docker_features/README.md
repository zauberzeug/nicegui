# Utilizing Docker signals and persistant storage.

This example shows how to utilize the features implemented into the NiceGUI release docker image. 
* Intercept signals passed from Docker to issue a graceful shutdown of NiceGUI.
* Volume mounting the .nicegui directory for persistant storage which will retain on container rebuild.

## Try it out.

Alter the docker-compose.yml file to your local host user's uid\gid and host storage path.

```bash
docker-compose up
```

Then you can access http://localhost:8080 and enter in data for storage. If you stop the container and look at the logs you should see it initiated ui.shutdown method.
