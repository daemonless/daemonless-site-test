# Mealie

Self-hosted recipe manager and meal planner on FreeBSD.

| | |
|---|---|
| **Port** | 9000 |
| **Registry** | `ghcr.io/daemonless/mealie` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/mealie](https://github.com/daemonless/mealie) |

!!! warning "Requires patched ocijail"
    This application requires the `allow.mlock` annotation.
    See [ocijail patch](../guides/ocijail-patch.md).

## Quick Start

=== "Podman CLI"

    ```bash
    podman run -d --name mealie \
      -p 9000:9000 \
      -v mealie-data:/app/data \
      ghcr.io/daemonless/mealie:latest
    ```
    
    Access at: http://localhost:9000
    Default login: `changeme@example.com` / `MyPassword`

=== "Compose"

    ```yaml
    services:
      mealie:
        image: ghcr.io/daemonless/mealie:latest
        container_name: mealie
        environment:
          - TZ=America/New_York
          - BASE_URL=https://mealie.example.com
        volumes:
          - mealie-data:/app/data
        ports:
          - 9000:9000
        restart: unless-stopped
    
    volumes:
      mealie-data:
    ```

## Quick Start - PostgreSQL

> **Requires [patched ocijail](https://github.com/daemonless/daemonless#ocijail-patch)** for SysV IPC support

```bash
# Create network
podman network create mealie-net

# Start PostgreSQL
podman run -d --name mealie-postgres \
  --network mealie-net \
  -e POSTGRES_USER=mealie \
  -e POSTGRES_PASSWORD=mealie \
  -e POSTGRES_DB=mealie \
  --annotation 'org.freebsd.jail.allow.sysvipc=true' \
  -v mealie-postgres:/var/db/postgres \
  ghcr.io/daemonless/postgres:17

# Start Mealie
podman run -d --name mealie \
  --network mealie-net \
  -p 9000:9000 \
  -e DB_ENGINE=postgres \
  -e POSTGRES_USER=mealie \
  -e POSTGRES_PASSWORD=mealie \
  -e POSTGRES_SERVER=mealie-postgres \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_DB=mealie \
  -v mealie-data:/app/data \
  ghcr.io/daemonless/mealie:latest
```

## podman-compose - PostgreSQL

> **Requires [patched ocijail](https://github.com/daemonless/daemonless#ocijail-patch)** for SysV IPC support

```yaml
services:
  mealie:
    image: ghcr.io/daemonless/mealie:latest
    container_name: mealie
    depends_on:
      - postgres
    environment:
      - TZ=America/New_York
      - BASE_URL=https://mealie.example.com
      - DB_ENGINE=postgres
      - POSTGRES_USER=mealie
      - POSTGRES_PASSWORD=mealie
      - POSTGRES_SERVER=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=mealie
    volumes:
      - mealie-data:/app/data
    ports:
      - 9000:9000
    restart: unless-stopped

  postgres:
    image: ghcr.io/daemonless/postgres:17
    container_name: mealie-postgres
    annotations:
      org.freebsd.jail.allow.sysvipc: "true"
    environment:
      - POSTGRES_USER=mealie
      - POSTGRES_PASSWORD=mealie
      - POSTGRES_DB=mealie
    volumes:
      - mealie-postgres:/var/db/postgres
    # healthcheck:  # Not yet supported on FreeBSD
    #   test: ["CMD", "pg_isready", "-q", "-d", "mealie", "-U", "mealie"]
    #   interval: 30s
    #   timeout: 20s
    #   retries: 3
    restart: unless-stopped

volumes:
  mealie-data:
  mealie-postgres:
```

## Tags

| Tag | Source | Description |
|-----|--------|-------------|
| `:latest` | [Upstream Releases](https://github.com/mealie-recipes/mealie) | Built from source |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TZ` | `UTC` | Timezone |
| `BASE_URL` | - | Public URL for the instance |
| `DB_ENGINE` | `sqlite` | Database engine (`sqlite` or `postgres`) |
| `ALLOW_SIGNUP` | `true` | Enable/disable user registration |

### PostgreSQL Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | - | Database user |
| `POSTGRES_PASSWORD` | - | Database password |
| `POSTGRES_SERVER` | - | Database hostname |
| `POSTGRES_PORT` | `5432` | Database port |
| `POSTGRES_DB` | - | Database name |

### OpenAI Integration

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_BASE_URL` | - | OpenAI-compatible API URL |
| `OPENAI_API_KEY` | - | API key |
| `OPENAI_MODEL` | - | Model name (e.g., `gpt-4o-mini`) |

## Volumes

| Path | Description |
|------|-------------|
| `/app/data` | Application data (recipes, images, SQLite DB) |

## Ports

| Port | Description |
|------|-------------|
| 9000 | Web UI |

## Notes

- **User:** `bsd` (UID/GID 1000)
- **PostgreSQL:** Requires `--annotation 'org.freebsd.jail.allow.sysvipc=true'`

## Links

- [Mealie Website](https://mealie.io/)
- [Mealie Documentation](https://docs.mealie.io/)
- [GitHub](https://github.com/mealie-recipes/mealie)
