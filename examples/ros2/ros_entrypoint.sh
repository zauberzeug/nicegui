#!/bin/bash
set -e

source /opt/ros/humble/setup.bash
source install/setup.bash

exec "$@"
