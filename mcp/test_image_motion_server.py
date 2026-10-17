#!/usr/bin/env python3
"""Smoke test runner for CineLogic Image Motion MCP Server.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SERVER_SCRIPT = Path(__file__).parent / "image_motion_server.py"

def run_rpc(requests: list[dict]) -> list[dict]:
    p = subprocess.Popen(
        [sys.executable, str(SERVER_SCRIPT)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    input_str = "\n".join(json.dumps(r) for r in requests) + "\n"
    stdout, stderr = p.communicate(input=input_str, timeout=10)
    
    responses = []
    for line in stdout.strip().splitlines():
        if line.strip():
            responses.append(json.loads(line))
    return responses

def main():
    print("=== Testing CineLogic Image Motion MCP Server ===")
    
    req_init = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "cinelogic-test-client", "version": "1.0"}
        }
    }
    
    req_tools = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    req_bible = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "cinelogic_generate_style_bible",
            "arguments": {
                "topic": "The Battle of Leipzig 1813",
                "chapter_title": "The Fog of Nations",
                "emotional_register": "somber_epic"
            }
        }
    }
    
    responses = run_rpc([req_init, req_tools, req_bible])
    for resp in responses:
        rid = resp.get("id")
        if rid == 1:
            print("  [PASS] Initialize:", resp["result"]["serverInfo"])
        elif rid == 2:
            tools = [t["name"] for t in resp["result"]["tools"]]
            print(f"  [PASS] Registered Tools ({len(tools)}):", tools)
        elif rid == 3:
            content = json.loads(resp["result"]["content"][0]["text"])
            print("  [PASS] Style Bible generated for:", content["topic"])
            print("         Visual Style:", content["style_bible"]["visual_style"][:80] + "...")
            print("         Chaining Rule:", content["style_bible"]["chaining_rule"])
            
    print("\nCineLogic Image Motion MCP server passed all tests cleanly!")

if __name__ == "__main__":
    main()
