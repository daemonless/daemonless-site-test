# Logging

daemonless containers use s6-log for internal log rotation.

## Log Locations

| Location | Description |
|----------|-------------|
| `/config/logs/daemonless/<app>/` | s6 system logs (stdout/stderr capture) |
| `/config/logs/` | Application-specific logs |
| `podman logs <container>` | Console output (still works) |

## Configuration

Control logging via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `S6_LOG_ENABLE` | `1` | Enable/disable file logging |
| `S6_LOG_MAX_SIZE` | `1048576` | Max size per log file (1MB) |
| `S6_LOG_MAX_FILES` | `10` | Number of rotated files to keep |

## Disable File Logging

If you only want `podman logs` output:

```bash
podman run -d --name radarr \
  -e S6_LOG_ENABLE=0 \
  ghcr.io/daemonless/radarr:latest
```

## View Logs

```bash
# Podman logs (live)
podman logs -f radarr

# s6 logs (rotated files)
tail -f /data/config/radarr/logs/daemonless/radarr/current

# Application logs
ls /data/config/radarr/logs/
```

## Log Rotation

s6-log automatically rotates when files reach `S6_LOG_MAX_SIZE`. Old logs are named with timestamps and kept up to `S6_LOG_MAX_FILES`.
