# Networking

FreeBSD Podman supports two networking modes for containers.

## Port Forwarding (Recommended)

```bash
podman run -d -p 7878:7878 --name radarr ghcr.io/daemonless/radarr:latest
```

Maps container port to host port. Requires pf configuration.

### pf.conf Setup

Add to `/etc/pf.conf`:

```
# Podman container networking
rdr-anchor "cni-rdr/*"
nat-anchor "cni-rdr/*"
table <cni-nat>
nat on $ext_if inet from <cni-nat> to any -> ($ext_if)
nat on $ext_if inet from 10.88.0.0/16 to any -> ($ext_if)
```

Enable local filtering:

```bash
sysctl net.pf.filter_local=1
echo 'net.pf.filter_local=1' >> /etc/sysctl.conf
pfctl -f /etc/pf.conf
```

### Multiple Ports

```bash
podman run -d \
  -p 80:80 \
  -p 443:443 \
  -p 8080:8080 \
  --name traefik ghcr.io/daemonless/traefik:latest
```

## Host Network

```bash
podman run -d --network=host --name radarr ghcr.io/daemonless/radarr:latest
```

Container shares the host's network namespace directly.

| Pros | Cons |
|------|------|
| Simpler setup | Less isolation |
| No pf config needed | Port conflicts possible |
| Better performance | Container sees all host interfaces |

## Container-to-Container

Containers on the default bridge network can communicate via IP. Use `podman inspect` to find container IPs:

```bash
podman inspect -f '{{.NetworkSettings.IPAddress}}' radarr
```
