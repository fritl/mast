#!/usr/bin/env bash
docker build \
      -t mast:latest \
     --build-arg VITE_GIT_COMMIT=$(git rev-parse --short HEAD) \
     --build-arg VITE_GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD) \
     --build-arg VITE_BUILD_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
     .
