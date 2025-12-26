# Development

Start contributing to the project or build your own custom images.

## Building Images Locally

The project includes a helper script to build images locally using the same logic as the CI pipeline.

### Prerequisites

- FreeBSD 15 host
- `podman` and `ocijail` installed

### Using local-build.sh

The `local-build.sh` script is located in `daemonless/scripts/`.

**Syntax:**
```bash
./scripts/local-build.sh <freebsd_version> [image_name] [tag]
```

**Examples:**

```bash
# Build ALL images for FreeBSD 15 (takes a long time)
./scripts/local-build.sh 15

# Build a specific image
./scripts/local-build.sh 15 radarr

# Build a specific image and tag
./scripts/local-build.sh 15 radarr latest
./scripts/local-build.sh 15 radarr pkg
```

## Creating a New Image

1.  **Create Directory**: Create a new directory for your service in `daemonless/<service_name>`.
2.  **Containerfile**: Create a `Containerfile` (see conventions below).
3.  **CI Configuration**: Add `.woodpecker.yml` (copy from an existing simple service like `tautulli`).

### Containerfile Conventions

- **Base Image**: Always start `FROM ghcr.io/daemonless/base:15` (or `arr-base`/`nginx-base`).
- **Use `fetch`**: FreeBSD base does not include `curl` or `wget`. Use `fetch` for downloading files.
- **Labels**: Use `org.opencontainers.image.*` labels.
- **Packages**:
    - Define packages in an `ARG PACKAGES` line for transparency.
    - Install using `pkg install -y ... && pkg clean -a`.

**Example:**
```dockerfile
FROM ghcr.io/daemonless/base:15

ARG PACKAGES="ca_root_nss"

RUN pkg install -y ${PACKAGES} && \
    pkg clean -a

# ... rest of build ...
```

## OCIjail Patching

If you are developing .NET applications or apps requiring specific jail permissions, you need the patched `ocijail`.

See the [My Custom Guide](ocijail-patch.md) for instructions on building and installing the patch.

## CI/CD Pipeline

Images are built using **Woodpecker CI**.

- **Trigger**: Push to `main` branch.
- **Build**: Podman builds the image.
- **Publish**: Pushes to `ghcr.io/daemonless/<image>`.

The pipeline logic is defined in `.woodpecker.yml` within each image directory.
