# Metadata Labels

daemonless uses container labels to provide structured information about images. These labels power documentation, the command generator, and CI/CD pipelines.

## Standard OCI Labels

We follow the [Open Container Initiative (OCI) Image Spec](https://github.com/opencontainers/image-spec/blob/main/annotations.md).

| Label | Description | Example |
|-------|-------------|---------|
| `org.opencontainers.image.title` | Human-readable title | `"radarr"` |
| `org.opencontainers.image.description` | Short description | `"Radarr movie management"` |
| `org.opencontainers.image.source` | Source code URL | `"https://github.com/daemonless/radarr"` |
| `org.opencontainers.image.url` | Application website | `"https://radarr.video/"` |
| `org.opencontainers.image.licenses` | License | `"GPL-3.0-only"` |
| `org.opencontainers.image.vendor` | Organization | `"daemonless"` |

## Daemonless Labels (`io.daemonless.*`)

### Image Metadata

| Label | Description | Example |
|-------|-------------|---------|
| `io.daemonless.port` | Primary port(s), comma-separated | `"7878"` or `"80,443"` |
| `io.daemonless.arch` | Supported architectures | `"amd64"` or `"amd64,arm64"` |
| `io.daemonless.volumes` | Default volumes, comma-separated | `"/movies,/downloads"` |
| `io.daemonless.config-mount` | Config directory (default: `/config`) | `"/gitea"` |
| `io.daemonless.category` | Image category for documentation | `"Media Management"` |
| `io.daemonless.packages` | Packages installed in image | `"${PACKAGES}"` |

### Build Control

| Label | Description | Example |
|-------|-------------|---------|
| `io.daemonless.wip` | Skip in CI/CD pipelines | `"true"` |
| `io.daemonless.pkg-source` | Use main Containerfile for `:pkg` tag | `"containerfile"` |
| `io.daemonless.base` | Required base image | `"nginx"` |
| `io.daemonless.network` | Required network mode | `"host"` |

### Upstream Version Tracking

| Label | Description | Example |
|-------|-------------|---------|
| `io.daemonless.upstream-mode` | Version check method | `"github"`, `"servarr"`, `"pkg"`, `"npm"` |
| `io.daemonless.upstream-repo` | GitHub repo | `"radarr/Radarr"` |
| `io.daemonless.upstream-url` | Version API URL | `"https://radarr.servarr.com/v1/..."` |
| `io.daemonless.upstream-package` | Package name for npm/pkg | `"n8n"` |
| `io.daemonless.upstream-branch` | Branch to track | `"develop"` |

### Upstream Mode Values

| Mode | Description |
|------|-------------|
| `github` | Check GitHub releases |
| `github_commits` | Track branch commits |
| `servarr` | Use Servarr update API |
| `sonarr` | Use Sonarr releases API |
| `pkg` | Track FreeBSD package version |
| `npm` | Check npm registry |
| `ubiquiti` | Check Ubiquiti firmware API |
| `source` | No upstream tracking |

## Why Labels Matter

1. **Command Generator** — The [interactive tool](../generator.md) reads labels to populate ports, volumes, and annotations
2. **Documentation** — This website uses labels to generate image documentation
3. **CI/CD** — Pipelines use `io.daemonless.wip` to skip work-in-progress images
4. **Version Tracking** — Upstream labels enable automated update detection

## Guidelines for Contributors

When adding a new image, include:

**Required:**

- `io.daemonless.port`
- `io.daemonless.arch`
- `io.daemonless.category`
- `io.daemonless.packages`

**Recommended:**

- `io.daemonless.upstream-mode` and related labels for version tracking
- `io.daemonless.volumes` if the app needs additional mounts
