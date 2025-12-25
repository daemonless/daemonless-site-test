# mealie

> **STATUS: BETA/WIP** - Requires Python 3.12+ (FreeBSD support emerging).

Self-hosted recipe manager and meal planner.

| | |
|---|---|
| **Port** | 9000 |
| **Registry** | `ghcr.io/daemonless/mealie` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/mealie](https://github.com/daemonless/mealie) |

!!! warning "Requires patched ocijail"
    This application requires the `allow.mlock` annotation.
    See [ocijail patch](../guides/ocijail-patch.md).

## Quick Start

```bash
podman run -d --name mealie \
  -p 9000:9000 \
  -e PUID=1000 -e PGID=1000 \
  --annotation 'org.freebsd.jail.allow.sysvipc=true' \
  -v /path/to/data:/app/data \
  -v /path/to/postgres:/var/db/postgres/data17 \
  ghcr.io/daemonless/mealie:latest
```

Access at: http://localhost:9000
Default login: `changeme@example.com` / `MyPassword`

## podman-compose

```yaml
services:
  mealie:
    image: ghcr.io/daemonless/mealie:latest
    container_name: mealie
    annotations:
      org.freebsd.jail.allow.sysvipc: "true"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
      - BASE_URL=https://mealie.example.com
    volumes:
      - /data/mealie/app:/app/data
      - /data/mealie/postgres:/var/db/postgres/data17
    ports:
      - 9000:9000
    restart: unless-stopped
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PUID` | 1000 | User ID for app |
| `PGID` | 1000 | Group ID for app |
| `TZ` | UTC | Timezone |
| `BASE_URL` | - | Public URL |

## Volumes

| Path | Description |
|------|-------------|
| `/app/data` | Application data |
| `/var/db/postgres/data17` | Embedded PostgreSQL data |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/mealie/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
