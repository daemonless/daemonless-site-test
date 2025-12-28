# Immich

Native FreeBSD port of [Immich](https://immich.app/) - the self-hosted photo and video management solution.

**Drop-in compatible** with official Linux Immich. Your existing data works unchanged.

| | |
|---|---|
| **Type** | Bundle / Stack |
| **Source** | [github.com/daemonless/immich](https://github.com/daemonless/immich) |

## Prerequisites

```bash
pkg install podman-suite cni-dnsname
```

The `cni-dnsname` package enables DNS resolution between containers, required for the Immich services to communicate.

## Quick Start

=== "Compose"

    1.  **Create directory and download compose file**:
        ```bash
        mkdir -p /containers/immich
        cd /containers/immich
        fetch https://raw.githubusercontent.com/daemonless/immich/main/container-compose.yml
        ```

    2.  **Create `.env` file**:
        ```bash
        cat > .env << 'EOF'
        UPLOAD_LOCATION=/containers/immich/library
        DB_PASSWORD=changeme
        DB_USERNAME=postgres
        DB_DATABASE_NAME=immich
        EOF
        ```

    3.  **Create library directory**:
        ```bash
        mkdir -p /containers/immich/library
        chown 1000:1000 /containers/immich/library
        ```

    4.  **Start the Stack**:
        ```bash
        podman-compose up -d
        ```

        Access the web interface at: http://localhost:2283

!!! warning "Absolute Paths Required"
    `UPLOAD_LOCATION` must be an absolute path (e.g., `/containers/immich/library`), not a relative path like `./library`.

## Architecture

This stack is composed of the following specialized FreeBSD containers:

| Service | Container Image | Description |
|---------|-----------------|-------------|
| **Server** | [`ghcr.io/daemonless/immich-server`](https://github.com/daemonless/immich-server) | Main Node.js application (Web/API) |
| **Database** | [`ghcr.io/daemonless/immich-postgres`](https://github.com/daemonless/immich-postgres) | PostgreSQL 14 with `pgvecto.rs` extension |
| **Redis** | [`ghcr.io/daemonless/redis`](https://github.com/daemonless/redis) | Redis cache (FreeBSD package) |
| **Machine Learning** | [`ghcr.io/daemonless/immich-ml`](https://github.com/daemonless/immich-ml) | Native ML service (CPU only) |

## Environment Variables

The stack relies on the standard Immich `.env` file. Key variables include:

| Variable | Description | Default |
|----------|-------------|---------|
| `UPLOAD_LOCATION` | Path on host to store photos/videos | `./library` |
| `DB_PASSWORD` | PostgreSQL password | `postgres` |
| `DB_USERNAME` | PostgreSQL user | `postgres` |
| `DB_DATABASE_NAME` | PostgreSQL database name | `immich` |
| `IMMICH_MACHINE_LEARNING_URL` | URL to ML service | *Required if external* |

## Ports

| Port | Service | Description |
|------|---------|-------------|
| `2283` | Server | Main Web UI and API |

## Volumes

| Path (Host) | Container Path | Description |
|-------------|----------------|-------------|
| `${UPLOAD_LOCATION}` | `/data` | Main media library |
| `pgdata` (Volume) | `/config/data` | Database files |
| `redis-data` (Volume) | `/config/data` | Redis persistence |

## Machine Learning

Immich Machine Learning is natively supported on FreeBSD. 

!!! note "CPU Only"
    Machine Learning on FreeBSD currently runs on the **CPU only**. Hardware acceleration (GPU/NPU) is not yet supported.

## Logging

Each container in this stack uses `s6-log` for log management:
- **Location:** Logs are stored inside each container at `/config/logs/`.
- **Access:** View logs via `podman logs -f <container_name>`.

## Migration from Linux

Migration is seamless as data formats are identical:

1.  Stop the Linux containers.
2.  Copy your `library`, `pgdata`, and `redis-data` volumes to the FreeBSD host.
3.  Update `UPLOAD_LOCATION` in `.env` to match the new FreeBSD path.
4.  Start the Daemonless containers.

## Links

- [Official Website](https://immich.app/)
- [Documentation](https://immich.app/docs)
- [GitHub Upstream](https://github.com/immich-app/immich)
