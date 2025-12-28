# unifi

UniFi Network Application for managing Ubiquiti network devices.

| | |
|---|---|
| **Port** | 8443 |
| **Registry** | `ghcr.io/daemonless/unifi` |
| **Tags** | `:latest`, `:pkg`, `:pkg-latest` |
| **Source** | [github.com/daemonless/unifi](https://github.com/daemonless/unifi) |

!!! warning "Requires patched ocijail"
    This application requires the `allow.mlock` annotation.
    See [ocijail patch](../guides/ocijail-patch.md).

## Quick Start

=== "Podman CLI"

    ```bash
    podman run -d --name unifi \
      --annotation 'org.freebsd.jail.allow.mlock=true' \
      --network host \
      -e PUID=1000 -e PGID=1000 \
      -v /path/to/config:/config \
      ghcr.io/daemonless/unifi:latest
    ```
    
    Access at: https://localhost:8443

=== "Compose"

    ```yaml
    services:
      unifi:
        image: ghcr.io/daemonless/unifi:latest
        container_name: unifi
        network_mode: host
        annotations:
          org.freebsd.jail.allow.mlock: "true"
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=America/New_York
        volumes:
          - /data/config/unifi:/config
        restart: unless-stopped
    ```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PUID` | 1000 | User ID for app |
| `PGID` | 1000 | Group ID for app |
| `TZ` | UTC | Timezone |
| `SYSTEM_IP` | - | Host IP for device inform (enables bridge networking) |

## Volumes

| Path | Description |
|------|-------------|--|
| `/config` | Configuration, database, and logs |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/unifi/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
