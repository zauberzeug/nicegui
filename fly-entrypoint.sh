#!/bin/bash
set -e

if [[ ! -z "$SWAP" ]]; then
  fallocate -l $(($(stat -f -c "(%a*%s/10)*7" .))) _swapfile
  mkswap _swapfile
  swapon _swapfile
fi

free -hm
df -h
exec "$@"
