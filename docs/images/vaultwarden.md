# vaultwarden

Bitwarden compatible backend server written in Rust, running natively on FreeBSD.

| | |
|---|---|
| **Port** | 80 |
| **Registry** | `ghcr.io/daemonless/vaultwarden` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/vaultwarden](https://github.com/daemonless/vaultwarden) |

## Quick Start

=== "Podman CLI"

    ```bash
    podman run -d --name vaultwarden \
      -p 80:80 \
      -e PUID=1000 -e PGID=1000 \
      -v /path/to/config:/config \
      ghcr.io/daemonless/vaultwarden:latest
    ```
    
    Access at: http://localhost

=== "Compose"

    ```yaml
    services:
      vaultwarden:
        image: ghcr.io/daemonless/vaultwarden:latest
        container_name: vaultwarden
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=America/New_York
        volumes:
          - /data/config/vaultwarden:/config
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

## Volumes

| Path | Description |
|------|-------------|
| `/config` | Configuration and data directory |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/vaultwarden/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
