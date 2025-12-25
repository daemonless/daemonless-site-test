# Available Images

All images are available at `ghcr.io/daemonless/<image>`.

## Media Management

| Image | Port | Description | .NET |
|-------|------|-------------|------|
| [Radarr](radarr.md) | 7878 | Movie collection manager | :material-check: |
| [Sonarr](sonarr.md) | 8989 | TV show collection manager | :material-check: |
| [Lidarr](lidarr.md) | 8686 | Music collection manager | :material-check: |
| [Readarr](readarr.md) | 8787 | Book collection manager | :material-check: |
| [Prowlarr](prowlarr.md) | 9696 | Indexer manager for *arr apps | :material-check: |
| [Overseerr](overseerr.md) | 5055 | Media request management | |

## Downloaders

| Image | Port | Description |
|-------|------|-------------|
| [SABnzbd](sabnzbd.md) | 8080 | Usenet downloader |
| [Transmission](transmission.md) | 9091 | BitTorrent client |
| [Transmission-WireGuard](transmission-wireguard.md) | 9091 | BitTorrent + WireGuard VPN |

## Media Servers

| Image | Port | Description |
|-------|------|-------------|
| [Jellyfin](jellyfin.md) | 8096 | Media streaming server |
| [Tautulli](tautulli.md) | 8181 | Plex monitoring and stats |

## Infrastructure

| Image | Port | Description |
|-------|------|-------------|
| [Traefik](traefik.md) | 80/443/8080 | Reverse proxy and load balancer |
| [Tailscale](tailscale.md) | — | Mesh VPN |
| [Gitea](gitea.md) | 3000 | Self-hosted Git service |
| [Woodpecker](woodpecker.md) | 8000 | CI/CD server |

## Utilities

| Image | Port | Description |
|-------|------|-------------|
| [Nextcloud](nextcloud.md) | 80 | File hosting and collaboration |
| [Mealie](mealie.md) | 9000 | Recipe manager |
| [n8n](n8n.md) | 5678 | Workflow automation |
| [UniFi](unifi.md) | 8443 | UniFi Network Controller |
| [Vaultwarden](vaultwarden.md) | 80 | Bitwarden-compatible password manager |
| [Organizr](organizr.md) | 80 | Service dashboard |
| [OpenSpeedTest](openspeedtest.md) | 3000 | Network speed test |
| [SmokePing](smokeping.md) | 80 | Network latency monitoring |

## Image Tags

All images support three tags:

| Tag | Package Source | Use Case |
|-----|----------------|----------|
| `:latest` | Upstream release | Newest features |
| `:pkg` | FreeBSD quarterly | Stable, well-tested |
| `:pkg-latest` | FreeBSD latest | Rolling updates |

## .NET Apps

Images marked with :material-check: in the .NET column require the `allow.mlock` annotation:

```bash
--annotation 'org.freebsd.jail.allow.mlock=true'
```

This requires the [patched ocijail](../guides/ocijail-patch.md).
