# tailscale

Mesh VPN container.

| | |
|---|---|
| **Registry** | `ghcr.io/daemonless/tailscale` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/tailscale](https://github.com/daemonless/tailscale) |

## Quick Start

```bash
podman run -d --name tailscale \
  --network none \
  --annotation 'org.freebsd.jail.vnet=new' \
  -v /containers/tailscale:/var/db/tailscale \
  --restart unless-stopped \
  ghcr.io/daemonless/tailscale:latest
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `S6_LOG_ENABLE` | Enable/Disable file logging | `1` |
| `S6_LOG_MAX_SIZE` | Max size per log file (bytes) | `1048576` |
| `S6_LOG_MAX_FILES` | Number of rotated log files to keep | `10` |

## Volumes

| Path | Description |
|------|-------------|
| `/var/db/tailscale` | State directory (identity, auth) |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/tailscale/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
