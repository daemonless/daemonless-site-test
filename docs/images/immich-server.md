# immich-server

Main application server (Node.js) for [Immich](https://immich.app/).

| | |
|---|---|
| **Port** | 2283 |
| **Registry** | `ghcr.io/daemonless/immich-server` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/immich-server](https://github.com/daemonless/immich-server) |

## Quick Start

=== "Podman CLI"

    ```bash
    podman run -d --name immich-server \
      -p 2283:2283 \
      -e DB_HOSTNAME=immich-postgres \
      -e DB_USERNAME=postgres \
      -e DB_PASSWORD=postgres \
      -e DB_DATABASE_NAME=immich \
      -e REDIS_HOSTNAME=redis \
      -v /containers/immich/upload:/usr/src/app/upload \
      -v /containers/immich/library:/usr/src/app/library \
      ghcr.io/daemonless/immich-server:latest
    ```

=== "Compose"

    ```yaml
    services:
      immich-server:
        image: ghcr.io/daemonless/immich-server:latest
        container_name: immich-server
        environment:
          - DB_HOSTNAME=immich-postgres
          - DB_USERNAME=postgres
          - DB_PASSWORD=postgres
          - DB_DATABASE_NAME=immich
          - REDIS_HOSTNAME=redis
        volumes:
          - /data/immich/upload:/usr/src/app/upload
          - /data/immich/library:/usr/src/app/library
        ports:
          - 2283:2283
        restart: unless-stopped
        depends_on:
          - immich-postgres
          - redis
    ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOSTNAME` | PostgreSQL hostname | - |
| `DB_USERNAME` | PostgreSQL username | - |
| `DB_PASSWORD` | PostgreSQL password | - |
| `DB_DATABASE_NAME` | PostgreSQL database name | - |
| `REDIS_HOSTNAME` | Redis hostname | - |
| `IMMICH_PORT` | Server listening port | `2283` |
| `UPLOAD_LOCATION` | Upload directory | `/usr/src/app/upload` |
| `IMMICH_MEDIA_LOCATION` | Media library directory | `/usr/src/app/library` |
| `IMMICH_MACHINE_LEARNING_URL` | URL to ML service (see Notes) | - |

## Volumes

| Path | Description |
|------|-------------|
| `/usr/src/app/upload` | Uploaded photos/videos |
| `/usr/src/app/library` | External library storage |
| `/config` | Configuration directory |
