# overseerr

Request management and media discovery tool for Plex.

| | |
|---|---|
| **Port** | 5055 |
| **Registry** | `ghcr.io/daemonless/overseerr` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/overseerr](https://github.com/daemonless/overseerr) |

## Quick Start

```bash
podman run -d --name overseerr \
  -p 5055:5055 \
  -e PUID=1000 -e PGID=1000 \
  -v /path/to/config:/config \
  ghcr.io/daemonless/overseerr:latest
```

Access at: http://localhost:5055

## podman-compose

```yaml
services:
  overseerr:
    image: ghcr.io/daemonless/overseerr:latest
    container_name: overseerr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
    volumes:
      - /data/config/overseerr:/config
    ports:
      - 5055:5055
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
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/overseerr/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
