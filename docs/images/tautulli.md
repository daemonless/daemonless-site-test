# Tautulli

Plex Media Server monitoring and statistics.

| | |
|---|---|
| **Port** | 8181 |
| **Registry** | `ghcr.io/daemonless/tautulli` |
| **Tags** | `:latest`, `:pkg`, `:pkg-latest` |
| **Source** | [github.com/daemonless/tautulli](https://github.com/daemonless/tautulli) |
| **Upstream** | [tautulli.com](https://tautulli.com) |

## Quick Start

```bash
podman run -d --name tautulli \
  -p 8181:8181 \
  -e PUID=1000 -e PGID=1000 \
  -v /data/config/tautulli:/config \
  ghcr.io/daemonless/tautulli:latest
```

No special annotations required — Tautulli is a Python application.

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
    restart: unless-stopped
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PUID` | `1000` | User ID for the application |
| `PGID` | `1000` | Group ID for the application |
| `TZ` | `UTC` | Timezone |

## Volumes

| Path | Description |
|------|-------------|
| `/config` | Configuration, database, and logs |

## Plex Integration

After starting, access the web UI at `http://localhost:8181` and follow the setup wizard to connect to your Plex server.
