# radarr

Movie collection manager for Usenet and BitTorrent users.

| | |
|---|---|
| **Port** | 7878 |
| **Registry** | `ghcr.io/daemonless/radarr` |
| **Tags** | `:latest`, `:pkg`, `:pkg-latest` |
| **Source** | [github.com/daemonless/radarr](https://github.com/daemonless/radarr) |

!!! warning "Requires patched ocijail"
    This application requires the `allow.mlock` annotation.
    See [ocijail patch](../guides/ocijail-patch.md).

## Quick Start

```bash
podman run -d --name radarr \
  -p 7878:7878 \
  --annotation 'org.freebsd.jail.allow.mlock=true' \
  -e PUID=1000 -e PGID=1000 \
  -v /path/to/config:/config \
  -v /path/to/movies:/movies \
  -v /path/to/downloads:/downloads \
  ghcr.io/daemonless/radarr:latest
```

Access at: http://localhost:7878

## podman-compose

```yaml
services:
  radarr:
    image: ghcr.io/daemonless/radarr:latest
    container_name: radarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
    volumes:
      - /data/config/radarr:/config
      - /data/media/movies:/movies
      - /data/downloads:/downloads
    ports:
      - 7878:7878
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
| `/movies` | Movie library |
| `/downloads` | Download directory |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/radarr/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
