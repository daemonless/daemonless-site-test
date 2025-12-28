# redis

Redis key-value store for [Immich](https://immich.app/) and other applications.

| | |
|---|---|
| **Port** | 6379 |
| **Registry** | `ghcr.io/daemonless/redis` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/redis](https://github.com/daemonless/redis) |

## Quick Start

=== "Podman CLI"

    ```bash
    podman run -d --name redis \
      -p 6379:6379 \
      -e PUID=1000 -e PGID=1000 \
      -v /path/to/config:/config \
      ghcr.io/daemonless/redis:latest
    ```

=== "Compose"

    ```yaml
    services:
      redis:
        image: ghcr.io/daemonless/redis:latest
        container_name: redis
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=America/New_York
        volumes:
          - /data/config/redis:/config
        ports:
          - 6379:6379
        restart: unless-stopped
    ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PUID` | User ID for the application process | `1000` |
| `PGID` | Group ID for the application process | `1000` |
| `TZ` | Timezone for the container | `UTC` |
| `S6_LOG_ENABLE` | Enable/Disable file logging | `1` |
| `S6_LOG_MAX_SIZE` | Max size per log file (bytes) | `1048576` |
| `S6_LOG_MAX_FILES` | Number of rotated log files to keep | `10` |
| `REDIS_DATA` | Data directory path | `/config/data` |

## Volumes

| Path | Description |
|------|-------------|
| `/config` | Configuration and data directory |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/redis/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
