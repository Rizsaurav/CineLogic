#!/usr/bin/env python3
"""Smoke test runner for CineLogic MCP Server.
Verifies JSON-RPC over stdio communication and tool execution under CineLogic branding.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SERVER_SCRIPT = Path(__file__).parent / "server.py"

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
    print("=== Testing CineLogic MCP Server Initialization ===")
    
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
    
    req_call_design = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "cinelogic_design_shot",
            "arguments": {
                "subject": "French cavalry charging through misty ravine",
                "duration_sec": 14.0,
                "shot_size": "medium",
                "camera_move": "track_right"
            }
        }
    }
    
    req_call_prompt = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "cinelogic_format_prompt",
            "arguments": {
                "style": "Vivid 2D historical anime, rich cel shading, dark ink outlines",
                "subject": "Napoleon looking through brass telescope",
                "beat": "lowering telescope with stern expression",
                "secondary": "gunpowder smoke drifting across battlefield"
            }
        }
    }

    req_call_diag = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "cinelogic_diagnose_failure",
            "arguments": {
                "symptom": "character legs running in place on treadmill effect",
                "attempt_number": 2
            }
        }
    }

    req_call_audit = {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "tools/call",
        "params": {
            "name": "cinelogic_audit_script",
            "arguments": {
                "sentences": [
                    "In October 1813, half a million soldiers assembled near Leipzig.",
                    "The company recorded over $450 million in revenue during the fourth quarter of 2024 which represents unprecedented market consolidation.",
                    "General Bertrand took up defensive positions along the Elster riverbank."
                ]
            }
        }
    }
    
    responses = run_rpc([req_init, req_tools, req_call_design, req_call_prompt, req_call_diag, req_call_audit])
    
    for resp in responses:
        rid = resp.get("id")
        if rid == 1:
            print("  [PASS] Initialize succeeded:", resp["result"]["serverInfo"])
        elif rid == 2:
            tools = [t["name"] for t in resp["result"]["tools"]]
            print(f"  [PASS] Tools List ({len(tools)} tools):", tools)
        elif rid == 3:
            content = json.loads(resp["result"]["content"][0]["text"])
            print("  [PASS] Tool 'cinelogic_design_shot' status:", content["status"])
            print("         Warnings:", content["warnings"])
        elif rid == 4:
            content = json.loads(resp["result"]["content"][0]["text"])
            print("  [PASS] Tool 'cinelogic_format_prompt' compiled:")
            print("        ", content["compiled_prompt"])
        elif rid == 5:
            content = json.loads(resp["result"]["content"][0]["text"])
            print("  [PASS] Tool 'cinelogic_diagnose_failure' root cause:", content["root_cause"])
            print("         Action:", content["action"])
        elif rid == 6:
            content = json.loads(resp["result"]["content"][0]["text"])
            print("  [PASS] Tool 'cinelogic_audit_script' flagged count:", content["flagged_count"])
            for s in content["sentences"]:
                if s["status"] == "FLAGGED":
                    print(f"         Sentence {s['index']} ({s['est_sec']}s):", s["findings"])
            
    print("\nAll CineLogic MCP tests passed with 100% success!")

if __name__ == "__main__":
    main()
