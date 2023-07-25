#!/bin/bash
set -x
# Get the PUID and PGID from environment variables (or use default values 1000 if not set)
PUID=${PUID:-1000}
PGID=${PGID:-1000}

# Check if the provided PUID and PGID are non-empty, numeric values; otherwise, assign default values
if ! [[ "$PUID" =~ ^[0-9]+$ ]]; then
  PUID=1000
fi

if ! [[ "$PGID" =~ ^[0-9]+$ ]]; then
  PGID=1000
fi

# Check if the specified group with PGID exists, if not, create it
if ! getent group "$PGID" >/dev/null; then
  groupadd -g "$PGID" appgroup
fi

useradd --create-home --shell /bin/bash --uid "$PUID" --gid "$PGID" appuser
chown -R appuser:appgroup /app
chmod -R 777 /usr/share/fonts
chmod -R 777 /var/cache/fontconfig
chmod -R 777 /usr/local/share/fonts

exec su appuser -p -c "cd /app && python main.py"