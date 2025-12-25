# readarr

Book and audiobook collection manager for Usenet and BitTorrent users.

| | |
|---|---|
| **Port** | 8787 |
| **Registry** | `ghcr.io/daemonless/readarr` |
| **Tags** | `:latest`, `:pkg`, `:pkg-latest` |
| **Source** | [github.com/daemonless/readarr](https://github.com/daemonless/readarr) |

!!! warning "Requires patched ocijail"
    This application requires the `allow.mlock` annotation.
    See [ocijail patch](../guides/ocijail-patch.md).

## Quick Start

```bash
podman run -d --name readarr \
  -p 8787:8787 \
  --annotation 'org.freebsd.jail.allow.mlock=true' \
  -e PUID=1000 -e PGID=1000 \
  -v /path/to/config:/config \
  -v /path/to/books:/books \
  -v /path/to/downloads:/downloads \
  ghcr.io/daemonless/readarr:latest
```

Access at: http://localhost:8787

## podman-compose

```yaml
services:
  readarr:
    image: ghcr.io/daemonless/readarr:latest
    container_name: readarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
    volumes:
      - /data/config/readarr:/config
      - /data/media/books:/books
      - /data/downloads:/downloads
    ports:
      - 8787:8787
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
| `/books` | Book library |
| `/downloads` | Download directory |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/readarr/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
