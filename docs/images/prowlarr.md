# prowlarr

Indexer manager/proxy for *arr applications.

| | |
|---|---|
| **Port** | 9696 |
| **Registry** | `ghcr.io/daemonless/prowlarr` |
| **Tags** | `:latest`, `:pkg`, `:pkg-latest` |
| **Source** | [github.com/daemonless/prowlarr](https://github.com/daemonless/prowlarr) |

!!! warning "Requires patched ocijail"
    This application requires the `allow.mlock` annotation.
    See [ocijail patch](../guides/ocijail-patch.md).

## Quick Start

=== "Podman CLI"

    ```bash
    podman run -d --name prowlarr \
      -p 9696:9696 \
      --annotation 'org.freebsd.jail.allow.mlock=true' \
      -e PUID=1000 -e PGID=1000 \
      -v /path/to/config:/config \
      ghcr.io/daemonless/prowlarr:latest
    ```
    
    Access at: http://localhost:9696

=== "Compose"

    ```yaml
    services:
      prowlarr:
        image: ghcr.io/daemonless/prowlarr:latest
        container_name: prowlarr
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=America/New_York
        volumes:
          - /data/config/prowlarr:/config
        ports:
          - 9696:9696
        annotations:
          org.freebsd.jail.allow.mlock: "true"
        restart: unless-stopped
    ```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PUID` | 1000 | User ID for app |
| `PGID` | 1000 | Group ID for app |
| `TZ` | UTC | Timezone |

## Volumes

| Path | Description |
|------|-------------|
| `/config` | Configuration directory |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/prowlarr/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
