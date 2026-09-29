#!/bin/bash

set -euo pipefail

IMAGE=go60-zmk-config-docker
BRANCH="${1:-4b2f3b9b718a4508e87111cdec24cda16f3c2726}"

docker build -t "$IMAGE" .
docker run --rm -v "$PWD:/config" -e UID="$(id -u)" -e GID="$(id -g)" -e BRANCH="$BRANCH" "$IMAGE"
