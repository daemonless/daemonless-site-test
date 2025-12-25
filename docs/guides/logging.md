# Logging

daemonless containers use s6-log for internal log rotation, ensuring persistent logs that survive container updates.

## How It Works

1. The application prints output to stdout/stderr
2. s6 pipes output to s6-log
3. s6-log saves to disk **and** mirrors to console so `podman logs` works

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
| `S6_LOG_STDOUT` | `1` | Mirror logs to console (`podman logs`) |
| `S6_LOG_DEST` | `/config/logs/daemonless` | Root directory for log storage |

## Examples

**Increase log retention:**

```bash
podman run -d -e S6_LOG_MAX_FILES=50 ghcr.io/daemonless/sonarr:latest
```

**Disable file logging (stdout only):**

```bash
podman run -d -e S6_LOG_ENABLE=0 ghcr.io/daemonless/sonarr:latest
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

By storing logs in `/config/logs/daemonless/`, your troubleshooting history survives container updates and recreations.
