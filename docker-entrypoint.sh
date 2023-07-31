#!/bin/bash

set -x
# Get the PUID and PGID from environment variables (or use default values 1000 if not set)
PUID=${PUID:-1000}
PGID=${PGID:-1000}

# Check if the provided PUID and PGID are non-empty, numeric values; otherwise, assign default values.
if ! [[ "$PUID" =~ ^[0-9]+$ ]]; then
  PUID=1000
fi
if ! [[ "$PGID" =~ ^[0-9]+$ ]]; then
  PGID=1000
fi
# Check if the specified group with PGID exists, if not, create it.
if ! getent group "$PGID" >/dev/null; then
  groupadd -g "$PGID" appgroup
fi
# Create user.
useradd --create-home --shell /bin/bash --uid "$PUID" --gid "$PGID" appuser
# Make user the owner of the app directory.
chown -R appuser:appgroup /app
# Set permissions on font directories.
if [ -d "/usr/share/fonts" ]; then
  chmod -R 777 /usr/share/fonts
fi
if [ -d "/var/cache/fontconfig" ]; then
  chmod -R 777 /var/cache/fontconfig
fi
if [ -d "/usr/local/share/fonts" ]; then
  chmod -R 777 /usr/local/share/fonts
fi
# Execute the application per the arguments to the file.
exec su appuser -p -c "$@"