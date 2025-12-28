# immich-postgres

PostgreSQL 14 with pgvector + VectorChord for [Immich](https://immich.app/).

Drop-in compatible with official Immich PostgreSQL image.

| | |
|---|---|
| **Port** | 5432 |
| **Registry** | `ghcr.io/daemonless/immich-postgres` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/immich-postgres](https://github.com/daemonless/immich-postgres) |

## Quick Start

=== "Podman CLI"

    ```bash
    podman run -d --name immich-postgres \
      --annotation 'org.freebsd.jail.allow.sysvipc=true' \
      -p 5432:5432 \
      -e POSTGRES_PASSWORD=postgres \
      -e POSTGRES_DB=immich \
      -v /containers/immich/postgres:/config \
      ghcr.io/daemonless/immich-postgres:latest
    ```
    
    **Note:** The `org.freebsd.jail.allow.sysvipc=true` annotation is required for PostgreSQL shared memory.

=== "Compose"

    ```yaml
    services:
      immich-postgres:
        image: ghcr.io/daemonless/immich-postgres:latest
        container_name: immich-postgres
        environment:
          - POSTGRES_PASSWORD=postgres
          - POSTGRES_DB=immich
        volumes:
          - /data/config/postgres:/config
        ports:
          - 5432:5432
        annotations:
          org.freebsd.jail.allow.sysvipc: "true"
        restart: unless-stopped
    ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | Database superuser name | `postgres` |
| `POSTGRES_PASSWORD` | Superuser password | `postgres` |
| `POSTGRES_DB` | Default database to create | `immich` |
| `PGDATA` | Data directory location | `/config/data` |

## Volumes

| Path | Description |
|------|-------------|
| `/config` | Configuration and data directory (PGDATA is in `/config/data`) |
