# transmission

Lightweight BitTorrent client with web interface.

| | |
|---|---|
| **Port** | 9091 |
| **Registry** | `ghcr.io/daemonless/transmission` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/transmission](https://github.com/daemonless/transmission) |

## Quick Start

```bash
podman run -d --name transmission \
  -p 9091:9091 \
  -p 51413:51413 \
  -p 51413:51413/udp \
  -e PUID=1000 -e PGID=1000 \
  -v /path/to/config:/config \
  -v /path/to/downloads:/downloads \
  -v /path/to/watch:/watch \
  ghcr.io/daemonless/transmission:latest
```

Access at: http://localhost:9091

## podman-compose

```yaml
services:
  transmission:
    image: ghcr.io/daemonless/transmission:latest
    container_name: transmission
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
    volumes:
      - /data/config/transmission:/config
      - /data/downloads:/downloads
      - /data/watch:/watch
    ports:
      - 9091:9091
      - 51413:51413
      - 51413:51413/udp
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
| `/downloads` | Download directory |
| `/watch` | Watch directory for .torrent files |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/transmission/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
