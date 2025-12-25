# tautulli

Monitoring, analytics, and notifications for Plex Media Server.

| | |
|---|---|
| **Port** | 8181 |
| **Registry** | `ghcr.io/daemonless/tautulli` |
| **Tags** | `:latest`, `:pkg`, `:pkg-latest` |
| **Source** | [github.com/daemonless/tautulli](https://github.com/daemonless/tautulli) |

## Quick Start

```bash
podman run -d --name tautulli \
  -p 8181:8181 \
  -e PUID=1000 -e PGID=1000 \
  -v /path/to/config:/config \
  --health-cmd /healthz \
  ghcr.io/daemonless/tautulli:latest
```

Access at: http://localhost:8181

## podman-compose

```yaml
services:
  tautulli:
    image: ghcr.io/daemonless/tautulli:latest
    container_name: tautulli
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
    volumes:
      - /data/config/tautulli:/config
    ports:
      - 8181:8181
    healthcheck:
      test: ["CMD", "/healthz"]
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
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/tautulli/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
