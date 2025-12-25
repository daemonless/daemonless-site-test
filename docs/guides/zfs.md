# ZFS Storage

Configure Podman to use ZFS on FreeBSD for container storage.

## Default Storage

By default, Podman uses `/var/db/containers` with the vfs storage driver.

## Configure ZFS Driver

Edit `/usr/local/etc/containers/storage.conf`:

```toml
[storage]
driver = "zfs"
graphroot = "/var/db/containers/storage"

[storage.options.zfs]
mountopt = "nodev"
```

## Create ZFS Dataset

```bash
# Create dataset for container storage
zfs create zroot/containers
zfs set mountpoint=/var/db/containers/storage zroot/containers

# Optional: enable compression
zfs set compression=lz4 zroot/containers
```

## Benefits

| Feature | Benefit |
|---------|---------|
| Copy-on-write | Fast container creation |
| Snapshots | Easy backup/restore |
| Compression | Smaller storage footprint |
| Checksums | Data integrity |

## Separate Config Storage

Keep container configs on a separate dataset for easy backup:

```bash
zfs create zroot/data/config
zfs set mountpoint=/data/config zroot/data/config

# Snapshot before upgrades
zfs snapshot zroot/data/config@before-upgrade
```

## Troubleshooting

### Permission Issues

```bash
# Ensure correct ownership
chown -R root:wheel /var/db/containers
```

### Reset Storage

```bash
# Stop all containers first
podman stop -a
podman system reset
```
