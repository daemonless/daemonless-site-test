# n8n

Workflow automation tool.

> **STATUS: WIP** - Native build with custom patching for FreeBSD.

| | |
|---|---|
| **Port** | 5678 |
| **Registry** | `ghcr.io/daemonless/n8n` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/n8n](https://github.com/daemonless/n8n) |

## Quick Start

```bash
podman run -d --name n8n \
  -p 5678:5678 \
  -e PUID=1000 -e PGID=1000 \
  -v /path/to/data:/config \
  ghcr.io/daemonless/n8n:latest
```

Access at: http://localhost:5678

## podman-compose

```yaml
services:
  n8n:
    image: ghcr.io/daemonless/n8n:latest
    container_name: n8n
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
      - N8N_HOST=n8n.example.com
      - WEBHOOK_URL=https://n8n.example.com/
    volumes:
      - /data/n8n:/config
    ports:
      - 5678:5678
    restart: unless-stopped
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PUID` | 1000 | User ID for app |
| `PGID` | 1000 | Group ID for app |
| `TZ` | UTC | Timezone |
| `N8N_ENCRYPTION_KEY` | - | Encryption key for credentials |
| `WEBHOOK_URL` | - | URL for webhooks |

## Volumes

| Path | Description |
|------|-------------|
| `/config` | n8n data (workflows, credentials, settings) |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/n8n/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
