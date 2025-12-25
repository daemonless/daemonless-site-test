# smokeping

Deluxe latency measurement tool.

| | |
|---|---|
| **Port** | 80 |
| **Registry** | `ghcr.io/daemonless/smokeping` |
| **Tags** | `:latest`, `:pkg`, `:pkg-latest` |
| **Source** | [github.com/daemonless/smokeping](https://github.com/daemonless/smokeping) |

## Quick Start

```bash
podman run -d --name smokeping \
  --network=host \
  -e PUID=1000 -e PGID=1000 \
  -v /path/to/config:/config \
  ghcr.io/daemonless/smokeping:latest
```

Access at: http://localhost:80/smokeping/smokeping.cgi

## podman-compose

```yaml
services:
  smokeping:
    image: ghcr.io/daemonless/smokeping:latest
    container_name: smokeping
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
    volumes:
      - /data/config/smokeping:/config
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
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/smokeping/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
