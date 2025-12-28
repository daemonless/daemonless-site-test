# jellyfin

The Free Software Media System

| | |
|---|---|
| **Port** | 8096 |
| **Registry** | `ghcr.io/daemonless/jellyfin` |
| **Tags** | `:latest`, `:pkg`, `:pkg-latest` |
| **Source** | [github.com/daemonless/jellyfin](https://github.com/daemonless/jellyfin) |

!!! warning "Requires patched ocijail"
    This application requires the `allow.mlock` annotation.
    See [ocijail patch](../guides/ocijail-patch.md).

## Quick Start

=== "Podman CLI"

    ```bash
    podman run -d --name jellyfin \
      -p 8096:8096 \
      -e PUID=1000 -e PGID=1000 \
      -v /path/to/config:/config \
      -v /path/to/cache:/cache \
      -v /path/to/media:/media \
      --annotation 'org.freebsd.jail.allow.mlock=true' \
      ghcr.io/daemonless/jellyfin:latest
    ```
    
    Access at: http://localhost:8096

=== "Compose"

    ```yaml
    services:
      jellyfin:
        image: ghcr.io/daemonless/jellyfin:latest
        container_name: jellyfin
        annotations:
          org.freebsd.jail.allow.mlock: "true"
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=America/New_York
        volumes:
          - /data/config/jellyfin:/config
          - /data/cache/jellyfin:/cache
          - /data/media:/media
        ports:
          - 8096:8096
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
| `/cache` | Cache directory |
| `/media` | Media directory |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/jellyfin/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
