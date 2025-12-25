# gitea

Self-hosted Git service.

**Note:** Gitea dropped FreeBSD binary releases in v1.25.x. This image uses the FreeBSD package (`pkg install gitea`).

| | |
|---|---|
| **Port** | 3000 |
| **Registry** | `ghcr.io/daemonless/gitea` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/gitea](https://github.com/daemonless/gitea) |

## Quick Start

```bash
podman run -d --name gitea \
  --network none \
  --annotation 'org.freebsd.jail.vnet=new' \
  -v /containers/gitea:/gitea \
  --restart unless-stopped \
  ghcr.io/daemonless/gitea:latest
```

Access at: http://localhost:3000

## podman-compose

```yaml
services:
  gitea:
    image: ghcr.io/daemonless/gitea:latest
    container_name: gitea
    annotations:
      org.freebsd.jail.vnet: "new"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
    volumes:
      - /data/gitea:/gitea
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
| `/gitea` | Configuration, repositories, and data |

### Directory Structure
- `/gitea/custom/conf/app.ini` - Configuration
- `/gitea/repos` - Git repositories
- `/gitea/data` - Data (avatars, etc.)
- `/gitea/log` - Logs

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/gitea/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
