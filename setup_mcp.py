#!/usr/bin/env python3
"""
CineLogic MCP Configuration Helper
Automatically generates and installs client configurations for Claude Desktop and Antigravity IDE
using the exact absolute paths of this local CineLogic repository.
"""

import argparse
import json
import os
import platform
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
STUDIO_SERVER = REPO_ROOT / "mcp" / "server.py"
MOTION_SERVER = REPO_ROOT / "mcp" / "image_motion_server.py"

def get_claude_config_path() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Windows":
        app_data = os.getenv("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        return Path(app_data) / "Claude" / "claude_desktop_config.json"
    else: # Linux
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"

def get_antigravity_config_path() -> Path:
    return Path.home() / ".gemini" / "config" / "mcp_config.json"

def generate_config_dict() -> dict:
    return {
        "mcpServers": {
            "cinelogic-studio": {
                "command": sys.executable,
                "args": [str(STUDIO_SERVER)],
                "env": {
                    "PYTHONUNBUFFERED": "1"
                }
            },
            "cinelogic-motion": {
                "command": sys.executable,
                "args": [str(MOTION_SERVER)],
                "env": {
                    "PYTHONUNBUFFERED": "1"
                }
            }
        }
    }

def update_json_config(target_file: Path, new_servers: dict) -> bool:
    target_file.parent.mkdir(parents=True, exist_ok=True)
    current_data = {}
    if target_file.exists():
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                current_data = json.load(f)
        except Exception:
            current_data = {}

    if "mcpServers" not in current_data:
        current_data["mcpServers"] = {}

    current_data["mcpServers"].update(new_servers["mcpServers"])

    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(current_data, f, indent=2)
    return True

def main():
    parser = argparse.ArgumentParser(description="Configure CineLogic MCP servers for Claude Desktop and Antigravity IDE.")
    parser.add_argument("--install-claude", action="store_true", help="Write configuration to Claude Desktop config file")
    parser.add_argument("--install-antigravity", action="store_true", help="Write configuration to Antigravity IDE config file")
    parser.add_argument("--json", action="store_true", help="Print only raw JSON configuration")
    
    args = parser.parse_args()
    config = generate_config_dict()

    if args.json:
        print(json.dumps(config, indent=2))
        return

    print("=" * 68)
    print("🎬 CineLogic Model Context Protocol (MCP) Configuration")
    print("=" * 68)
    print(f"Repository Root:   {REPO_ROOT}")
    print(f"Studio Server:     {STUDIO_SERVER}")
    print(f"Motion Server:     {MOTION_SERVER}")
    print(f"Python Binary:     {sys.executable}")
    print("=" * 68)

    installed = False

    if args.install_claude:
        c_path = get_claude_config_path()
        update_json_config(c_path, config)
        print(f"✓ Successfully updated Claude Desktop configuration at:")
        print(f"  {c_path}")
        installed = True

    if args.install_antigravity:
        a_path = get_antigravity_config_path()
        update_json_config(a_path, config)
        print(f"✓ Successfully updated Antigravity IDE configuration at:")
        print(f"  {a_path}")
        installed = True

    if not installed:
        print("\nReady-to-copy JSON snippet for your mcp_config.json:\n")
        print(json.dumps(config, indent=2))
        print("\nTip: To automatically write this configuration to your local clients, run:")
        print("  python3 setup_mcp.py --install-claude")
        print("  python3 setup_mcp.py --install-antigravity")

if __name__ == "__main__":
    main()
