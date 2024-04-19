#!/bin/bash
set -e

free -hm
df -h
exec "$@"
