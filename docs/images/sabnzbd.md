# sabnzbd

Binary newsreader for Usenet with NZB support.

| | |
|---|---|
| **Port** | 8080 |
| **Registry** | `ghcr.io/daemonless/sabnzbd` |
| **Tags** | `:latest`, `:pkg`, `:pkg-latest` |
| **Source** | [github.com/daemonless/sabnzbd](https://github.com/daemonless/sabnzbd) |

## Quick Start

=== "Podman CLI"

    ```bash
    podman run -d --name sabnzbd \
      -p 8080:8080 \
      -e PUID=1000 -e PGID=1000 \
      -v /path/to/config:/config \
      -v /path/to/downloads:/downloads \
      ghcr.io/daemonless/sabnzbd:latest
    ```
    
    Access at: http://localhost:8080

=== "Compose"

    ```yaml
    services:
      sabnzbd:
        image: ghcr.io/daemonless/sabnzbd:latest
        container_name: sabnzbd
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=America/New_York
          - HOST_WHITELIST=myserver,myserver.local
        volumes:
          - /data/config/sabnzbd:/config
          - /data/downloads:/downloads
        ports:
          - 8080:8080
        restart: unless-stopped
    ```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PUID` | 1000 | User ID for app |
| `PGID` | 1000 | Group ID for app |
| `TZ` | UTC | Timezone |
| `HOST_WHITELIST` | | Hostnames for initial config |

## Volumes

| Path | Description |
|------|-------------|
| `/config` | Configuration directory |
| `/downloads` | Download directory |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/sabnzbd/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
