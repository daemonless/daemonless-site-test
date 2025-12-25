# transmission-wireguard

Transmission BitTorrent client running through a WireGuard VPN tunnel on FreeBSD.

| | |
|---|---|
| **Port** | 9091 |
| **Registry** | `ghcr.io/daemonless/transmission-wireguard` |
| **Tags** | `:latest` |
| **Source** | [github.com/daemonless/transmission-wireguard](https://github.com/daemonless/transmission-wireguard) |

## Quick Start

```bash
podman run -d --name transmission-vpn \
  --annotation 'org.freebsd.jail.vnet=new' \
  -e WG_PRIVATE_KEY="your-private-key" \
  -e WG_PEER_PUBLIC_KEY="vpn-server-public-key" \
  -e WG_ENDPOINT="vpn.example.com:51820" \
  -e PUID=1000 -e PGID=1000 \
  -v /path/to/config:/config \
  -v /path/to/downloads:/downloads \
  ghcr.io/daemonless/transmission-wireguard:latest
```

**Access:** Check IP with `podman inspect transmission-vpn --format '{{.NetworkSettings.IPAddress}}'` then go to `http://<IP>:9091`.

## podman-compose

```yaml
services:
  transmission-vpn:
    image: ghcr.io/daemonless/transmission-wireguard:latest
    container_name: transmission-vpn
    environment:
      - WG_PRIVATE_KEY=your-private-key
      - WG_PEER_PUBLIC_KEY=vpn-server-public-key
      - WG_ENDPOINT=vpn.example.com:51820
      - WG_ADDRESS=10.5.0.2/32
      - WG_DNS=1.1.1.1
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
    volumes:
      - /data/config/transmission-vpn:/config
      - /data/downloads:/downloads
      - /data/watch:/watch
    annotations:
      org.freebsd.jail.vnet: "new"
    restart: unless-stopped
```

## Volumes

| Path | Description |
|------|-------------|
| `/config` | Configuration directory |
| `/downloads` | Download directory |
| `/watch` | Watch directory |

## Logging

This image uses `s6-log` for internal log rotation.
- **System Logs**: Captured from console and stored at `/config/logs/daemonless/transmission-wireguard/`.
- **Application Logs**: Managed by the app and typically found in `/config/logs/`.
- **Podman Logs**: Output is mirrored to the console, so `podman logs` still works.
