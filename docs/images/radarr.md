# Radarr

Movie collection manager for Usenet and BitTorrent users.

| | |
|---|---|
| **Port** | 7878 |
| **Registry** | `ghcr.io/daemonless/radarr` |
| **Tags** | `:latest`, `:pkg`, `:pkg-latest` |
| **Source** | [github.com/daemonless/radarr](https://github.com/daemonless/radarr) |
| **Upstream** | [radarr.video](https://radarr.video) |

!!! warning "Requires patched ocijail"
    Radarr is a .NET application and requires the `allow.mlock` annotation.
    See [ocijail patch](../guides/ocijail-patch.md).

## Quick Start

```bash
podman run -d --name radarr \
  -p 7878:7878 \
  --annotation 'org.freebsd.jail.allow.mlock=true' \
  -e PUID=1000 -e PGID=1000 \
  -v /data/config/radarr:/config \
  -v /data/media/movies:/movies \
  -v /data/downloads:/downloads \
  ghcr.io/daemonless/radarr:latest
```

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
| `PUID` | `1000` | User ID for the application |
| `PGID` | `1000` | Group ID for the application |
| `TZ` | `UTC` | Timezone |
| `S6_LOG_ENABLE` | `1` | Enable file logging |
| `S6_LOG_MAX_SIZE` | `1048576` | Max log file size (bytes) |
| `S6_LOG_MAX_FILES` | `10` | Number of rotated logs to keep |

## Volumes

| Path | Description |
|------|-------------|
| `/config` | Configuration and database |
| `/movies` | Movie library |
| `/downloads` | Download client output |

## Logging

| Location | Description |
|----------|-------------|
| `/config/logs/daemonless/radarr/` | s6 system logs |
| `/config/logs/` | Application logs |
| `podman logs radarr` | Console output |
