#!/usr/bin/env python3
"""
Sync documentation from repositories to website.
Scans cloned repos and parses Containerfile labels to generate docs/images/*.md files.
"""

import os
import re
from pathlib import Path
from typing import Optional

# Constants
REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs" / "images"
REPOS_DIR = REPO_ROOT.parent / "repos"

# Base images to skip (no user-facing docs)
SKIP_REPOS = {"base", "arr-base", "nginx-base"}


def parse_containerfile_labels(containerfile: Path) -> dict:
    """Parse labels from a Containerfile."""
    labels = {}
    if not containerfile.exists():
        return labels

    content = containerfile.read_text()

    # Match io.daemonless.* labels
    pattern = r'io\.daemonless\.([a-z-]+)="([^"]*)"'
    for match in re.finditer(pattern, content):
        key = match.group(1)
        value = match.group(2)
        # Handle ${PACKAGES} or similar ARG references
        if value.startswith("${"):
            continue
        labels[key] = value

    # Match org.opencontainers.image.title for display name
    title_match = re.search(r'org\.opencontainers\.image\.title="([^"]*)"', content)
    if title_match:
        labels["title"] = title_match.group(1)

    return labels


def get_image_tags(repo_path: Path) -> list[str]:
    """Determine available tags based on Containerfile variants."""
    tags = ["latest"]
    if (repo_path / "Containerfile.pkg").exists():
        tags.append("pkg")
        tags.append("pkg-latest")
    return tags


def discover_images() -> dict:
    """Scan repos directory and build image metadata from Containerfiles."""
    images = {}

    if not REPOS_DIR.exists():
        print(f"Repos directory not found: {REPOS_DIR}")
        return images

    for repo_path in sorted(REPOS_DIR.iterdir()):
        if not repo_path.is_dir():
            continue

        name = repo_path.name
        if name in SKIP_REPOS:
            continue

        containerfile = repo_path / "Containerfile"
        if not containerfile.exists():
            continue

        labels = parse_containerfile_labels(containerfile)

        # Skip WIP images
        if labels.get("wip") == "true":
            continue

        images[name] = {
            "category": labels.get("category", "Uncategorized"),
            "port": labels.get("port"),
            "tags": get_image_tags(repo_path),
            "title": labels.get("title", name.title()),
        }

    return images


def parse_readme_sections(content: str) -> dict[str, str]:
    """Parse markdown content into sections based on H2 headers."""
    sections = {}
    current_section = "intro"
    buffer = []

    for line in content.splitlines():
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


def extract_port(sections: dict[str, str], labels_port: Optional[str]) -> Optional[str]:
    """Extract port number from labels or README sections."""
    # Prefer Containerfile label
    if labels_port:
        return labels_port.split(",")[0]  # First port if multiple

    # Fallback to README parsing
    if "ports" in sections:
        match = re.search(r"\|\s*(\d+)\s*\|", sections["ports"])
        if match:
            return match.group(1)

    if "quick start" in sections:
        match = re.search(r"-p\s+(\d+):", sections["quick start"])
        if match:
            return match.group(1)

    return None


def generate_header_table(image_name: str, config: dict, port: Optional[str]) -> str:
    """Generate the summary table at the top of the page."""
    rows = []

    if port:
        rows.append(f"| **Port** | {port} |")

    registry = f"`ghcr.io/daemonless/{image_name}`"
    rows.append(f"| **Registry** | {registry} |")

    tags = [f"`:{tag}`" for tag in config.get("tags", ["latest"])]
    rows.append(f"| **Tags** | {', '.join(tags)} |")

    rows.append(f"| **Source** | [github.com/daemonless/{image_name}](https://github.com/daemonless/{image_name}) |")

    return "\n".join([
        "| | |",
        "|---|---|",
        *rows
    ])


def process_image(name: str, config: dict):
    """Process a single image and generate its documentation page."""
    repo_path = REPOS_DIR / name
    readme_path = repo_path / "README.md"

    if not readme_path.exists():
        print(f"Skipping {name}: README not found")
        return

    print(f"Processing {name}...")

    content = readme_path.read_text()

    # Extract title (H1)
    title_match = re.match(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1) if title_match else name.capitalize()

    sections = parse_readme_sections(content)

    # Clean intro: remove H1
    intro = sections.get("intro", "")
    intro = re.sub(r"^#\s+.*$\n", "", intro, flags=re.MULTILINE).strip()

    port = extract_port(sections, config.get("port"))

    # Build new content
    new_content = [f"# {title}\n", intro + "\n"]

    # Header Table
    new_content.append(generate_header_table(name, config, port) + "\n")

    # Special Warnings (ocijail)
    notes = sections.get("notes", "")
    if "ocijail" in notes.lower() or "mlock" in notes.lower():
        new_content.append('!!! warning "Requires patched ocijail"\n    This application requires the `allow.mlock` annotation.\n    See [ocijail patch](../guides/ocijail-patch.md).\n')

    # Quick Start
    if "quick start" in sections:
        new_content.append("## Quick Start\n")
        new_content.append(sections["quick start"] + "\n")

    # Podman Compose
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
    out_path.write_text("\n".join(new_content))


def generate_nav_entries(images: dict) -> list[str]:
    """Generate the YAML lines for the Images navigation section."""
    lines = ["  - Images:", "    - Overview: images/index.md"]

    # Group by category
    by_category: dict[str, list[str]] = {}
    for name, config in images.items():
        category = config.get("category", "Uncategorized")
        by_category.setdefault(category, []).append(name)

    # Sort categories and items
    for category in sorted(by_category.keys()):
        lines.append(f"    - {category}:")
        for name in sorted(by_category[category]):
            display_name = images[name].get("title", name.title())
            lines.append(f"      - {display_name}: images/{name}.md")

    return lines


def update_mkdocs_yml(images: dict):
    """Update the Images section in mkdocs.yml."""
    mkdocs_path = REPO_ROOT / "mkdocs.yml"
    lines = mkdocs_path.read_text().splitlines()

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
            # Check if we exited Images section (next top-level nav item)
            if re.match(r"^  - \w", line) and "Overview:" not in line:
                in_images = False
                new_lines.append(line)
        else:
            new_lines.append(line)

    mkdocs_path.write_text("\n".join(new_lines) + "\n")


def main():
    images = discover_images()

    if not images:
        print("No images found. Run fetch_repos.py first.")
        return

    print(f"Found {len(images)} images")

    # Sync docs
    for name, config in images.items():
        process_image(name, config)

    # Update mkdocs navigation
    update_mkdocs_yml(images)

    print("Done.")


if __name__ == "__main__":
    main()
