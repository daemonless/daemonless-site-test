# Uptime Kuma

A fancy self-hosted monitoring tool, running natively on FreeBSD.

| | |
|---|---|
| **Port** | 3001 |
| **Registry** | `ghcr.io/daemonless/uptime-kuma` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/uptime-kuma](https://github.com/daemonless/uptime-kuma) |

## Quick Start

=== "Podman CLI"

    ```bash
    podman run -d --name uptime-kuma \
      --annotation 'org.freebsd.jail.allow.raw_sockets=true' \
      -v /containers/uptime-kuma:/config \
      -p 3001:3001 \
      ghcr.io/daemonless/uptime-kuma:latest
    ```
    
    Access the web UI at `http://localhost:3001`

## Volumes

| Path | Description |
|------|-------------|
| `/config` | Database and configuration |
