# Architecture

How daemonless container images are structured and built.

## Image Layers

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontSize': '16px' }}}%%
flowchart LR
    subgraph base_layer["Base Layer"]
        base["base<br/>s6, execline"]
    end

    subgraph intermediate["Intermediate Layers"]
        arr-base["arr-base<br/><small>sqlite3, icu, libunwind...</small>"]
        nginx-base["nginx-base<br/><small>nginx</small>"]
    end

    subgraph arr_apps[".NET Apps"]
        lidarr["lidarr"]
        prowlarr["prowlarr"]
        radarr["radarr"]
        readarr["readarr"]
        sonarr["sonarr"]
    end

    subgraph nginx_apps["Nginx Apps"]
        nextcloud["nextcloud"]
        openspeedtest["openspeedtest"]
        organizr["organizr"]
        smokeping["smokeping"]
        vaultwarden["vaultwarden"]
    end

    subgraph base_apps["Direct Apps"]
        gitea["gitea"]
        jellyfin["jellyfin"]
        mealie["mealie"]
        n8n["n8n"]
        overseerr["overseerr"]
        sabnzbd["sabnzbd"]
        tailscale["tailscale"]
        tautulli["tautulli"]
        traefik["traefik"]
        transmission["transmission"]
        transmission-wireguard["transmission-wireguard"]
        unifi["unifi"]
        woodpecker["woodpecker"]
    end

    %% Connections
    base --> arr-base
    base --> nginx-base
    arr-base --> radarr
    arr-base --> sonarr
    arr-base --> prowlarr
    arr-base --> lidarr
    arr-base --> readarr
    nginx-base --> openspeedtest
    nginx-base --> organizr
    nginx-base --> smokeping
    nginx-base --> nextcloud
    nginx-base --> vaultwarden
    base --> sabnzbd
    base --> tautulli
    base --> jellyfin
    base --> transmission
    base --> transmission-wireguard
    base --> gitea
    base --> tailscale
    base --> traefik
    base --> mealie
    base --> n8n
    base --> overseerr
    base --> unifi
    base --> woodpecker

    %% Styling
    classDef baseStyle fill:#ab2b28,stroke:#333,color:#fff
    classDef intermediateStyle fill:#d35400,stroke:#333,color:#fff
    classDef appStyle fill:#2980b9,stroke:#333,color:#fff
    class base baseStyle
    class arr-base,nginx-base intermediateStyle
    class radarr,sonarr,prowlarr,lidarr,readarr,openspeedtest,organizr,smokeping,nextcloud,vaultwarden,sabnzbd,tautulli,jellyfin,transmission,transmission-wireguard,gitea,tailscale,traefik,mealie,n8n,overseerr,unifi,woodpecker appStyle
```

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

