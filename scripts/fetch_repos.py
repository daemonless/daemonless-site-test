#!/usr/bin/env python3
"""
Fetch all image repositories defined in dependencies.json.
Clones them into the ../repos directory.
"""

import json
import os
import subprocess
from pathlib import Path

# Constants
REPO_ROOT = Path(__file__).parent.parent
DEPS_FILE = REPO_ROOT / "dependencies.json"
TARGET_REPOS_DIR = REPO_ROOT.parent / "repos"

def load_dependencies() -> dict:
    """Load dependencies.json"""
    with open(DEPS_FILE) as f:
        return json.load(f)

def run_command(cmd: list, cwd: Path = None):
    """Run a shell command."""
    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd)

def main():
    deps = load_dependencies()
    images = deps.get("images", {})
    
    # Ensure target directory exists
    os.makedirs(TARGET_REPOS_DIR, exist_ok=True)
    
    # Default organization
    default_org = "daemonless"
    
    # Process each image
    for name, config in images.items():
        # Determine repo URL. Default to daemonless/<name>
        # Check if upstream override exists in dependencies.json (not fully implemented in structure but good practice)
        # For now, assume all our images match the pattern daemonless/<name>
        repo_url = f"https://github.com/{default_org}/{name}.git"
        
        target_path = TARGET_REPOS_DIR / name
        
        if target_path.exists():
            print(f"Skipping {name}: {target_path} already exists")
            continue
            
        print(f"Fetching {name} from {repo_url}...")
        try:
            run_command(["git", "clone", "--depth", "1", repo_url, str(target_path)])
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone {name}: {e}")
            # Optionally continue or fail. For CI, maybe failing is better?
            # But maybe some reponames don't match?
            # Let's try to be robust.
            pass

if __name__ == "__main__":
    main()
