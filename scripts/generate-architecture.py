#!/usr/bin/env python3
"""
Generate Mermaid diagram from dependencies.json

Usage:
    python3 scripts/generate-architecture.py > docs/architecture.md
    python3 scripts/generate-architecture.py --mermaid-only  # Just the diagram
"""

import json
import sys
from pathlib import Path

def load_dependencies(path: str = "dependencies.json") -> dict:
    """Load dependencies.json from repo root or specified path."""
    # Try multiple locations
    for p in [path, f"../{path}", f"../../daemonless/{path}"]:
        try:
            with open(p) as f:
                return json.load(f)
        except FileNotFoundError:
            continue
    raise FileNotFoundError(f"Could not find {path}")

def generate_mermaid(deps: dict) -> str:
    """Generate Mermaid flowchart from dependencies."""
    lines = [
        "```mermaid",
        "flowchart TB",
        "    subgraph base_layer[\"Base Layer\"]",
        "        base[\"base<br/><small>s6, execline</small>\"]",
        "    end",
        "",
    ]

    # Intermediate layers
    lines.append("    subgraph intermediate[\"Intermediate Layers\"]")

    base_images = deps.get("base_images", {})
    for name, info in base_images.items():
        if name == "base":
            continue
        packages = ", ".join(info.get("packages", [])[:3])
        if len(info.get("packages", [])) > 3:
            packages += "..."
        lines.append(f'        {name}["{name}<br/><small>{packages}</small>"]')

    lines.append("    end")
    lines.append("")

    # Application layers grouped by parent
    arr_apps = []
    nginx_apps = []
    base_apps = []

    for name, info in deps.get("images", {}).items():
        parent = info.get("parent", "base")
        if parent == "arr-base":
            arr_apps.append(name)
        elif parent == "nginx-base":
            nginx_apps.append(name)
        else:
            base_apps.append(name)

    # Arr apps subgraph
    if arr_apps:
        lines.append("    subgraph arr_apps[\".NET Apps\"]")
        for app in sorted(arr_apps):
            lines.append(f'        {app}["{app}"]')
        lines.append("    end")
        lines.append("")

    # Nginx apps subgraph
    if nginx_apps:
        lines.append("    subgraph nginx_apps[\"Nginx Apps\"]")
        for app in sorted(nginx_apps):
            lines.append(f'        {app}["{app}"]')
        lines.append("    end")
        lines.append("")

    # Base apps subgraph
    if base_apps:
        lines.append("    subgraph base_apps[\"Direct Apps\"]")
        for app in sorted(base_apps):
            lines.append(f'        {app}["{app}"]')
        lines.append("    end")
        lines.append("")

    # Connections
    lines.append("    %% Connections")
    lines.append("    base --> arr-base")
    lines.append("    base --> nginx-base")

    for app in arr_apps:
        lines.append(f"    arr-base --> {app}")

    for app in nginx_apps:
        lines.append(f"    nginx-base --> {app}")

    for app in base_apps:
        lines.append(f"    base --> {app}")

    # Styling
    lines.append("")
    lines.append("    %% Styling")
    lines.append("    classDef baseStyle fill:#ab2b28,stroke:#333,color:#fff")
    lines.append("    classDef intermediateStyle fill:#d35400,stroke:#333,color:#fff")
    lines.append("    classDef appStyle fill:#2980b9,stroke:#333,color:#fff")
    lines.append("    class base baseStyle")
    lines.append("    class arr-base,nginx-base intermediateStyle")

    all_apps = arr_apps + nginx_apps + base_apps
    lines.append(f"    class {','.join(all_apps)} appStyle")

    lines.append("```")

    return "\n".join(lines)

def generate_page(deps: dict) -> str:
    """Generate full architecture page with mermaid diagram."""
    mermaid = generate_mermaid(deps)

    page = f"""# Architecture

How daemonless container images are structured and built.

## Image Layers

{mermaid}

## Layer Descriptions

### Base Layer

The `base` image provides the foundation for all daemonless containers:

- **FreeBSD 15** (or 14) minimal base
- **s6** - Process supervision
- **execline** - Scripting language for s6
- **FreeBSD-utilities** - Core utilities

### Intermediate Layers

| Image | Purpose | Key Packages |
|-------|---------|--------------|
| **arr-base** | .NET runtime for *arr apps | sqlite3, icu, libunwind, .NET compat |
| **nginx-base** | Web server base | nginx |

### Application Layer

Final images that users run. Each inherits from either:

- `base` - Direct apps (Python, Go, Node.js apps)
- `arr-base` - .NET applications (Radarr, Sonarr, etc.)
- `nginx-base` - PHP/web applications (Nextcloud, Organizr, etc.)

## Build Order

When a base image changes, dependent images must be rebuilt:

1. **base** changes → rebuild everything
2. **arr-base** changes → rebuild *arr apps only
3. **nginx-base** changes → rebuild nginx apps only

This is handled automatically by the [cascade rebuild workflow](https://github.com/daemonless/daemonless/blob/main/.github/workflows/trigger-cascade.yml).

## Image Inheritance

```
FreeBSD 15 Base
└── base (s6, execline)
    ├── arr-base (sqlite3, icu, .NET compat)
    │   ├── radarr
    │   ├── sonarr
    │   ├── prowlarr
    │   ├── lidarr
    │   └── readarr
    ├── nginx-base (nginx)
    │   ├── nextcloud
    │   ├── organizr
    │   ├── openspeedtest
    │   ├── smokeping
    │   └── vaultwarden
    ├── transmission
    ├── tautulli
    ├── sabnzbd
    ├── jellyfin
    ├── gitea
    ├── traefik
    ├── tailscale
    ├── overseerr
    ├── mealie
    ├── n8n
    ├── unifi
    └── woodpecker
```
"""
    return page

def main():
    mermaid_only = "--mermaid-only" in sys.argv

    deps = load_dependencies()

    if mermaid_only:
        print(generate_mermaid(deps))
    else:
        print(generate_page(deps))

if __name__ == "__main__":
    main()
