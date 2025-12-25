# Init System (s6)

daemonless containers use s6-svscan for process supervision, handling multi-process containers and flexible runtime configuration.

## The /init Script

The entrypoint for all containers. Responsibilities:

1. **Environment Handling** — Captures environment variables for supervised services
2. **Networking** — Configures loopback interface (`lo0`) for health checks
3. **Initialization** — Executes startup scripts in order
4. **Supervision** — Starts s6-svscan to manage processes

## Initialization Sequence

When a container starts, `/init` runs scripts from these directories in order:

### 1. Built-in Init (/etc/cont-init.d/)

Part of the container image. Handles:

- Configuring the `bsd` user (PUID/PGID)
- Setting permissions on `/config`
- Generating default configuration files

### 2. Custom Init (/custom-cont-init.d/)

User-provided scripts. Mount your scripts here to run custom initialization:

```bash
podman run -d \
  -v /path/to/my-scripts:/custom-cont-init.d:ro \
  ghcr.io/daemonless/radarr:latest
```

## Service Management

Processes are supervised by s6. If an application crashes, s6 automatically restarts it.

### Service Definitions

Services are defined in `/etc/services.d/<service-name>/run` — an executable script that launches the process in the foreground.

### Activating Services

Services must be symlinked into `/run/s6/services/`. This is handled during image build:

```dockerfile
RUN ln -sf /etc/services.d/myapp/run /run/s6/services/myapp/run
```

## Logging

Services output to stdout/stderr, captured by Podman:

```bash
podman logs <container-name>
```

See [Logging](logging.md) for s6-log configuration.

## Why s6?

Benefits of using [s6](https://skarnet.org/software/s6/):

- **Zombies** — Properly reaps zombie processes
- **Reliability** — Restarts failed services automatically
- **Flexibility** — Run helper processes (PostgreSQL, nginx) alongside the main app
- **PUID/PGID** — Drop privileges while still performing root-level init tasks
