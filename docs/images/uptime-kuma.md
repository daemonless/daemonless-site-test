# Uptime Kuma

A fancy self-hosted monitoring tool.

| | |
|---|---|
| **Port** | 3001 |
| **Registry** | `ghcr.io/daemonless/uptime-kuma` |
| **Tags** | `:latest`, `:pkg`, `:pkg-latest` |
| **Source** | [github.com/daemonless/uptime-kuma](https://github.com/daemonless/uptime-kuma) |

## Quick Start

```bash
podman run -d --name uptime-kuma \
  -p 3001:3001 \
  --annotation 'org.freebsd.jail.allow.raw_sockets=true' \
  -e PUID=1000 -e PGID=1000 \
  -v /containers/uptime-kuma:/config \
  ghcr.io/daemonless/uptime-kuma:latest
```

Access at: http://localhost:3001

!!! warning "Raw Sockets Required"
    **Ping monitoring** requires the `allow.raw_sockets` jail annotation. Without this, ICMP pings will fail.

## podman-compose

```yaml
services:
  uptime-kuma:
    image: ghcr.io/daemonless/uptime-kuma:latest
    container_name: uptime-kuma
    ports:
      - 3001:3001
    annotations:
      org.freebsd.jail.allow.raw_sockets: "true"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=UTC
    volumes:
      - /containers/uptime-kuma:/config
    restart: unless-stopped
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PUID` | 1000 | User ID for app |
| `PGID` | 1000 | Group ID for app |
| `TZ` | UTC | Timezone |
| `DATA_DIR` | /config | Internal data path |

## Volumes

| Path | Description |
|------|-------------|
| `/config` | Database and configuration |

## Browser Monitoring
This image includes Chromium for "Browser Engine" monitoring types. This increases the image size but allows for full page load checks.

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/uptime-kuma/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.

```