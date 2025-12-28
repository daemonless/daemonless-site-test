# organizr

HTPC/Homelab Services Organizer - dashboard for all your self-hosted services.

| | |
|---|---|
| **Port** | 80 |
| **Registry** | `ghcr.io/daemonless/organizr` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/organizr](https://github.com/daemonless/organizr) |

## Quick Start

=== "Podman CLI"

    ```bash
    podman run -d --name organizr \
      -p 80:80 \
      -e PUID=1000 -e PGID=1000 \
      -v /path/to/config:/config \
      ghcr.io/daemonless/organizr:latest
    ```
    
    Access at: http://localhost

=== "Compose"

    ```yaml
    services:
      organizr:
        image: ghcr.io/daemonless/organizr:latest
        container_name: organizr
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=America/New_York
          - BRANCH=v2-master
        volumes:
          - /data/config/organizr:/config
        ports:
          - 80:80
        restart: unless-stopped
    ```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PUID` | 1000 | User ID for app |
| `PGID` | 1000 | Group ID for app |
| `TZ` | UTC | Timezone |
| `BRANCH` | v2-master | Git branch (v2-master or v2-develop) |

## Volumes

| Path | Description |
|------|-------------|
| `/config` | Configuration directory (includes nginx/php configs) |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/organizr/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
