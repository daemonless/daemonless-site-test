# Container Fleet

Explore our collection of high-performance, FreeBSD-native OCI containers.

## Infrastructure

| Image | Port | Description |
|-------|------|-------------|
| [:simple-gitea: Gitea](gitea.md) | 3000 | Gitea self-hosted Git service on FreeBSD |
| [:simple-tailscale: Tailscale](tailscale.md) | None | Tailscale mesh VPN on FreeBSD |
| [:material-router-network: Traefik](traefik.md) | 80,443,8080 | Traefik reverse proxy on FreeBSD |
| [:material-hammer: Woodpecker](woodpecker.md) | None | Woodpecker CI server and agent |

## Media Management

| Image | Port | Description | .NET |
|-------|------|-------------|------|
| [:material-music: Lidarr](lidarr.md) | 8686 | Lidarr music management on FreeBSD | :material-check: |
| [:material-eye: Overseerr](overseerr.md) | 5055 | Overseerr media request management on FreeBSD |  |
| [:material-magnet: Prowlarr](prowlarr.md) | 9696 | Prowlarr indexer management on FreeBSD | :material-check: |
| [:material-movie: Radarr](radarr.md) | 7878 | Radarr movie management on FreeBSD | :material-check: |
| [:material-book: Readarr](readarr.md) | 8787 | Readarr ebook management on FreeBSD | :material-check: |
| [:material-television: Sonarr](sonarr.md) | 8989 | Sonarr TV show management on FreeBSD | :material-check: |

## Downloaders

| Image | Port | Description |
|-------|------|-------------|
| [:material-download-network: SABnzbd](sabnzbd.md) | 8080 | SABnzbd Usenet downloader on FreeBSD |
| [:simple-transmission: Transmission](transmission.md) | 9091 | Transmission BitTorrent client on FreeBSD |

## Media Servers

| Image | Port | Description |
|-------|------|-------------|
| [:simple-jellyfin: Jellyfin](jellyfin.md) | 8096 | The Free Software Media System on FreeBSD |
| [:simple-plex: Tautulli](tautulli.md) | 8181 | Tautulli Plex monitoring on FreeBSD |

## Utilities

| Image | Port | Description |
|-------|------|-------------|
| [:simple-nextcloud: Nextcloud](nextcloud.md) | 80 | Nextcloud self-hosted cloud on FreeBSD |
| [:material-speedometer: OpenSpeedTest](openspeedtest.md) | 3000 | HTML5 Network Speed Test on FreeBSD |
| [:material-view-dashboard: Organizr](organizr.md) | 80 | HTPC/Homelab Services Organizer on FreeBSD |
| [:material-pulse: SmokePing](smokeping.md) | 80 | SmokePing network latency monitor on FreeBSD |
| [:simple-ubiquiti: UniFi](unifi.md) | 8443 | UniFi Network Application on FreeBSD |
| [:material-chart-line: Uptime Kuma](uptime-kuma.md) | 3001 | A fancy self-hosted monitoring tool on FreeBSD |
| [:simple-bitwarden: Vaultwarden](vaultwarden.md) | 80 | Vaultwarden (Bitwarden compatible backend) on FreeBSD |

## Uncategorized

| Image | Port | Description |
|-------|------|-------------|
| [:simple-wireguard: Transmission WireGuard](transmission-wireguard.md) | 9091 | Transmission BitTorrent client with WireGuard VPN on FreeBSD |

## Image Tags

| Tag | Source | Description |
|-----|--------|-------------|
| `:latest` | Upstream releases | Newest version from project |
| `:pkg` | FreeBSD quarterly | Stable, tested in ports |
| `:pkg-latest` | FreeBSD latest | Rolling package updates |
