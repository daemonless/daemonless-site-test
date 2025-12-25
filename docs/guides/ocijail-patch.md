# ocijail Patch

.NET applications require the `allow.mlock` jail parameter. Stock ocijail doesn't support this — you need the patched version.

## Why This Is Needed

FreeBSD jails have `allow.*` parameters controlling permitted operations. Some applications require specific permissions:

| Parameter | Required By | Purpose |
|-----------|-------------|---------|
| `allow.mlock` | .NET apps (Radarr, Sonarr, etc.) | Memory locking for GC |
| `allow.raw_sockets` | Ping tools, Uptime Kuma | ICMP functionality |

## Installation

```bash
# Requires bazel and git
pkg install bazel git

# Clone and build
git clone https://github.com/dfr/ocijail /tmp/ocijail
cd /tmp/ocijail

# Apply patch (from daemonless repo)
fetch -o - https://raw.githubusercontent.com/daemonless/daemonless/main/scripts/ocijail-allow-annotations.patch | patch -p1

# Build
bazel build //...

# Install (backs up original)
cp /usr/local/bin/ocijail /usr/local/bin/ocijail.orig
cp bazel-bin/ocijail /usr/local/bin/ocijail
```

Or use the script from daemonless:

```bash
fetch -o - https://raw.githubusercontent.com/daemonless/daemonless/main/scripts/build-ocijail.sh | sh
```

## Usage

After patching, use annotations to enable jail parameters:

```bash
# For .NET apps
podman run -d --name radarr \
  --annotation 'org.freebsd.jail.allow.mlock=true' \
  ghcr.io/daemonless/radarr:latest

# For ping functionality
podman run -d --name uptime-kuma \
  --annotation 'org.freebsd.jail.allow.raw_sockets=true' \
  localhost/uptime-kuma:latest
```

## Supported Annotations

Any `allow.*` jail parameter works:

| Annotation | Jail Parameter |
|------------|----------------|
| `org.freebsd.jail.allow.mlock=true` | `allow.mlock` |
| `org.freebsd.jail.allow.raw_sockets=true` | `allow.raw_sockets` |
| `org.freebsd.jail.allow.chflags=true` | `allow.chflags` |

See `jail(8)` for all available parameters.

## Upstream Status

This patch has not been submitted upstream. Stock ocijail supports `org.freebsd.jail.vnet` but not the generic `allow.*` parameters.
