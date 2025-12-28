# woodpecker

Continuous Integration (CI) server and agent.

| | |
|---|---|
| **Port** | 8000 |
| **Registry** | `ghcr.io/daemonless/woodpecker` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/woodpecker](https://github.com/daemonless/woodpecker) |

## Quick Start

=== "Compose"

    ```yaml
    services:
      woodpecker-server:
        image: ghcr.io/daemonless/woodpecker:latest
        container_name: woodpecker-server
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=America/New_York
          - WOODPECKER_SERVER_ENABLE=true
          - WOODPECKER_GITEA=true
          - WOODPECKER_GITEA_URL=https://gitea.example.com
          - WOODPECKER_AGENT_SECRET=changeme
        volumes:
          - /data/woodpecker:/var/lib/woodpecker
        ports:
          - 8000:8000
          - 9000:9000
        restart: unless-stopped
    
      woodpecker-agent:
        image: ghcr.io/daemonless/woodpecker:latest
        container_name: woodpecker-agent
        environment:
          - PUID=1000
          - PGID=1000
          - WOODPECKER_AGENT_ENABLE=true
          - WOODPECKER_SERVER=woodpecker-server:9000
          - WOODPECKER_AGENT_SECRET=changeme
        volumes:
          - /var/run/podman/podman.sock:/var/run/podman.sock
        restart: unless-stopped
    ```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PUID` | 1000 | User ID for app |
| `PGID` | 1000 | Group ID for app |
| `TZ` | UTC | Timezone |
| `WOODPECKER_SERVER_ENABLE` | false | Enable server mode |
| `WOODPECKER_AGENT_ENABLE` | false | Enable agent mode |

See [Woodpecker Docs](https://woodpecker-ci.org/docs/administration/server-config) for all configuration options.

## Volumes

| Path | Description |
|------|-------------|
| `/var/lib/woodpecker` | Server database and data |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/woodpecker/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
