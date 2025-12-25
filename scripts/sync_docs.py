#!/usr/bin/env python3
"""
Sync documentation from repositories to website.
Reads dependencies.json and repository READMEs to generate docs/images/*.md files.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

# Constants
REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs" / "images"
REPOS_DIR = REPO_ROOT.parent / "repos"
DEPS_FILE = REPO_ROOT / "dependencies.json"

def load_dependencies() -> dict:
    """Load dependencies.json"""
    with open(DEPS_FILE) as f:
        return json.load(f)

def parse_readme_sections(content: str) -> Dict[str, str]:
    """Parse markdown content into sections based on H2 headers."""
    sections = {}
    current_section = "intro"
    lines = content.splitlines()
    buffer = []
    
    for line in lines:
        if line.startswith("## "):
            if buffer:
                sections[current_section] = "\n".join(buffer).strip()
            current_section = line[3:].strip().lower()
            buffer = []
        else:
            buffer.append(line)
            
    if buffer:
        sections[current_section] = "\n".join(buffer).strip()
        
    return sections

def extract_port(sections: Dict[str, str]) -> Optional[str]:
    """Extract port number from Ports or Quick Start sections."""
    # Try Ports section first
    if "ports" in sections:
        match = re.search(r"\|\s*(\d+)\s*\|", sections["ports"])
        if match:
            return match.group(1)
            
    # Try Quick Start section
    if "quick start" in sections:
        match = re.search(r"-p\s+(\d+):\1", sections["quick start"])
        if match:
            return match.group(1)
            
    return None

def generate_header_table(image_name: str, config: Dict[str, Any], port: Optional[str]) -> str:
    """Generate the summary table at the top of the page."""
    rows = []
    
    if port:
        rows.append(f"| **Port** | {port} |")
        
    registry = f"`ghcr.io/daemonless/{image_name}`"
    rows.append(f"| **Registry** | {registry} |")
    
    tags = []
    if "tags" in config:
        for tag in config["tags"]:
            tags.append(f"`:{tag}`")
    if tags:
        rows.append(f"| **Tags** | {', '.join(tags)} |")
        
    # Source link
    rows.append(f"| **Source** | [github.com/daemonless/{image_name}](https://github.com/daemonless/{image_name}) |")
    
    # Upstream link
    # This is trickier as it's not always in dependencies.json in a clean way, 
    # but we can try to guess or leave it if not found.
    # dependencies.json has "upstream_sources" but it's separate.
    
    return "\n".join([
        "| | |",
        "|---|---|",
        *rows
    ])

def process_image(name: str, config: Dict[str, Any], upstream_config: Dict[str, Any]):
    """Process a single image and generate its documentation page."""
    repo_path = REPOS_DIR / name
    readme_path = repo_path / "README.md"
    
    if not readme_path.exists():
        print(f"Skipping {name}: README not found at {readme_path}")
        return

    print(f"Processing {name}...")
    
    with open(readme_path) as f:
        content = f.read()
        
    # Extract title (H1)
    title_match = re.match(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1) if title_match else name.capitalize()
    
    sections = parse_readme_sections(content)
    
    # Extract intro (everything before first H2)
    # The parse_readme_sections handles this as "intro" key, but excludes the H1 title line if we strip it first.
    # Actually my parser includes H1 in intro if I didn't strip it.
    # Let's clean up intro: remove H1
    intro = sections.get("intro", "")
    intro = re.sub(r"^#\s+.*$\n", "", intro, flags=re.MULTILINE).strip()
    
    port = extract_port(sections)
    
    # Build new content
    new_content = []
    new_content.append(f"# {title}\n")
    new_content.append(intro + "\n")
    
    # Header Table
    new_content.append(generate_header_table(name, config, port) + "\n")
    
    # Special Warnings (e.g. ocijail)
    # Check if "Specific Requirements" or similar exists in Notes
    notes = sections.get("notes", "")
    if "ocijail" in notes.lower() or "mlock" in notes.lower():
         new_content.append('!!! warning "Requires patched ocijail"\n    This application requires the `allow.mlock` annotation.\n    See [ocijail patch](../guides/ocijail-patch.md).\n')

    # Quick Start
    if "quick start" in sections:
        new_content.append("## Quick Start\n")
        new_content.append(sections["quick start"] + "\n")
        
    # Docker/Podman Compose
    if "podman-compose" in sections:
        new_content.append("## podman-compose\n")
        new_content.append(sections["podman-compose"] + "\n")
    elif "docker-compose" in sections:
        new_content.append("## podman-compose\n")
        new_content.append(sections["docker-compose"] + "\n")

    # Environment Variables
    if "environment variables" in sections:
        new_content.append("## Environment Variables\n")
        new_content.append(sections["environment variables"] + "\n")

    # Volumes
    if "volumes" in sections:
        new_content.append("## Volumes\n")
        new_content.append(sections["volumes"] + "\n")

    # Logging
    if "logging" in sections:
        new_content.append("## Logging\n")
        new_content.append(sections["logging"] + "\n")
        
    # Write output
    out_path = DOCS_DIR / f"{name}.md"
    os.makedirs(out_path.parent, exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(new_content))

def generate_nav_entries(images: Dict[str, Any]) -> List[str]:
    """Generate the YAML lines for the Images navigation section."""
    lines = ["  - Images:", "    - Overview: images/index.md"]
    
    # Group by category
    by_category = {}
    for name, config in images.items():
        category = config.get("category", "Uncategorized")
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(name)
        
    # Sort categories and items
    for category in sorted(by_category.keys()):
        lines.append(f"    - {category}:")
        for name in sorted(by_category[category]):
            # Use title case for name, but keep specific capitalizations if we knew them.
            # For now capitalize first letter.
            display_name = name # Default to key
            
            # Simple heuristic for better names
            if name == "n8n": display_name = "n8n" # Special case
            elif name == "openspeedtest": display_name = "OpenSpeedTest"
            elif name == "traefik": display_name = "Traefik"
            elif name == "tailscale": display_name = "Tailscale"
            elif name == "gitea": display_name = "Gitea"
            elif name == "woodpecker": display_name = "Woodpecker"
            elif name == "sabnzbd": display_name = "SABnzbd"
            elif name == "unifi": display_name = "UniFi"
            else: display_name = name.title() # Radarr, Sonarr, etc.
            
            lines.append(f"      - {display_name}: images/{name}.md")
            
    return lines

def update_mkdocs_yml(images: Dict[str, Any]):
    """Update the Images section in mkdocs.yml."""
    mkdocs_path = REPO_ROOT / "mkdocs.yml"
    with open(mkdocs_path) as f:
        lines = f.read().splitlines()
        
    new_lines = []
    in_images = False
    images_processed = False
    
    for line in lines:
        if line.strip() == "- Images:":
            in_images = True
            if not images_processed:
                new_lines.extend(generate_nav_entries(images))
                images_processed = True
            continue
            
        if in_images:
            # Check if we exited Images section
            # The next section will start with "  - " (2 spaces indent)
            if line.startswith("  - ") and not line.strip().startswith("- Overview:") and not line.strip().startswith("- Media Management:"): 
               # Needed more robust check. 
               # Previous file had:
               #   - Images:
               #     - Overview...
               #   - Guides:
               # So if we see "  - " again, we left.
               in_images = False
               new_lines.append(line)
            else:
                # collecting old images lines, skip them
                pass
        else:
            new_lines.append(line)
            
    with open(mkdocs_path, "w") as f:
        f.write("\n".join(new_lines) + "\n")

def main():
    deps = load_dependencies()
    images = deps.get("images", {})
    upstream = deps.get("upstream_sources", {})
    
    # Sync docs
    for name, config in images.items():
        process_image(name, config, upstream.get(name, {}))
        
    # Update mkdocs
    update_mkdocs_yml(images)

if __name__ == "__main__":
    main()
