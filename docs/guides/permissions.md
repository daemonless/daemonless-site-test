# Permissions (PUID/PGID)

All daemonless containers support running as a non-root user via `PUID` and `PGID` environment variables.

## Why Use PUID/PGID?

By default, processes in containers run as root. This can cause permission issues when mounting host directories:

- Files created by the container are owned by root
- The container may not have access to files owned by your user
- Security implications of running as root

## How It Works

When you set `PUID=1000` and `PGID=1000`:

1. The container creates a user with UID 1000 and GID 1000
2. The application runs as this user
3. Files are created with matching ownership

## Finding Your UID/GID

```bash
id $USER
# uid=1000(ahze) gid=1000(ahze) groups=1000(ahze),0(wheel)
```

## Usage

```bash
podman run -d --name radarr \
  -e PUID=1000 \
  -e PGID=1000 \
  -v /data/config/radarr:/config \
  ghcr.io/daemonless/radarr:latest
```

## Common Issues

### Permission Denied

If the container can't write to mounted volumes:

```bash
# Check current ownership
ls -la /data/config/radarr

# Fix ownership
chown -R 1000:1000 /data/config/radarr
```

### NFS Mounts

For NFS, ensure the UID/GID matches across systems. All daemonless containers default to `1000:1000` for consistent NFS access.
