# daemonless

**Native FreeBSD OCI containers** — Like [LinuxServer.io](https://linuxserver.io), but for FreeBSD.

Production-ready container images using Podman and ocijail.

## Features

- **s6 process supervision** — Reliable init system for containers
- **PUID/PGID support** — Run as any user, not just root
- **FreeBSD 14 & 15** — Support for current releases
- **Minimal images** — Cleaned pkg cache, small footprint
- **Port forwarding** — Full `-p` flag support with pf

## Quick Example

```bash
podman run -d --name radarr \
  -p 7878:7878 \
  --annotation 'org.freebsd.jail.allow.mlock=true' \
  -e PUID=1000 -e PGID=1000 \
  -v /data/config/radarr:/config \
  ghcr.io/daemonless/radarr:latest
```

## Available Images

Over 20 images available:

| Category | Images |
|----------|--------|
| **Media Management** | Radarr, Sonarr, Lidarr, Readarr, Prowlarr, Overseerr |
| **Downloaders** | SABnzbd, Transmission, Transmission-WireGuard |
| **Media Servers** | Jellyfin, Tautulli |
| **Infrastructure** | Traefik, Tailscale, Gitea, Woodpecker CI |
| **Utilities** | Nextcloud, Mealie, n8n, UniFi, Vaultwarden |

[View all images :material-arrow-right:](images/index.md)

## Image Tags

| Tag | Source | Description |
|-----|--------|-------------|
| `:latest` | Upstream releases | Newest version from project |
| `:pkg` | FreeBSD quarterly | Stable, tested in ports |
| `:pkg-latest` | FreeBSD latest | Rolling package updates |

## Getting Started

<div class="grid cards" markdown>

-   :material-rocket-launch: **Quick Start**

    ---

    Get your first container running in 5 minutes

    [:octicons-arrow-right-24: Quick Start](quick-start.md)

-   :material-book-open-variant: **Image Docs**

    ---

    Full documentation for each container image

    [:octicons-arrow-right-24: Images](images/index.md)

-   :material-console: **Command Generator**

    ---

    Interactive tool to build podman run commands

    [:octicons-arrow-right-24: Generator](generator.md)

</div>
