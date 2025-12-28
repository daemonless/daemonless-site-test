# gitea

Self-hosted Git service.

| | |
|---|---|
| **Port** | 3000 |
| **Registry** | `ghcr.io/daemonless/gitea` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/gitea](https://github.com/daemonless/gitea) |

## Quick Start

=== "Podman CLI"

    ```bash
    podman run -d --name gitea \
      -p 3000:3000 -p 2222:22 \
      -e PUID=1000 -e PGID=1000 \
      -v /data/gitea:/gitea \
      ghcr.io/daemonless/gitea:latest
    ```
    
    Access at: http://localhost:3000

=== "Compose"

    ```yaml
    services:
      gitea:
        image: ghcr.io/daemonless/gitea:latest
        container_name: gitea
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=America/New_York
        volumes:
          - /data/gitea:/gitea
        ports:
          - 3000:3000
          - 2222:22
        restart: unless-stopped
    ```

=== "Ansible"

    ```yaml
    - name: Deploy Gitea
      containers.podman.podman_container:
        name: gitea
        image: ghcr.io/daemonless/gitea:latest
        state: started
        restart_policy: unless-stopped
        env:
          PUID: "1000"
          PGID: "1000"
          TZ: "America/New_York"
        ports:
          - "3000:3000"
          - "2222:22"
        volumes:
          - /data/gitea:/gitea
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
