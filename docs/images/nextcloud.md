# nextcloud

Self-hosted productivity platform (file sync, share, collaboration).

| | |
|---|---|
| **Port** | 80 |
| **Registry** | `ghcr.io/daemonless/nextcloud` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/nextcloud](https://github.com/daemonless/nextcloud) |

## Quick Start

```bash
podman run -d --name nextcloud \
  --network=host \
  -e PUID=1000 -e PGID=1000 \
  -v /path/to/config:/config \
  -v /path/to/data:/data \
  ghcr.io/daemonless/nextcloud:latest
```

Access at: http://localhost:80

## podman-compose

```yaml
services:
  nextcloud:
    image: ghcr.io/daemonless/nextcloud:latest
    container_name: nextcloud
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
    volumes:
      - /data/config/nextcloud:/config
      - /data/nextcloud:/data
    network_mode: host
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
| `/config` | Configuration (nginx.conf, config.php) |
| `/data` | User data files |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/nextcloud/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
