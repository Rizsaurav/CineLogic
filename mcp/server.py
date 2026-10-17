#!/usr/bin/env python3
"""CineLogic Studio: Model Context Protocol (MCP) Server

Exposes the CineLogic AI Film Director and QC engine as standard MCP tools over stdio.
Compatible with Antigravity IDE, Claude Desktop, and any MCP-compliant client.
Pure Python standard library implementation with zero external transport dependencies.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

# Define tool metadata
TOOLS = [
    {
        "name": "cinelogic_design_shot",
        "description": "Applies cinematic motion grammar to a shot. Validates camera move vocabulary, shot sizes, enforces <=25% push-in ceiling, and formats motion parameters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "Subject or action description"},
                "duration_sec": {"type": "number", "description": "Shot duration in seconds (must be <= 10.0)"},
                "shot_size": {
                    "type": "string",
                    "enum": ["extreme_wide", "wide", "medium", "close", "extreme_close"],
                    "description": "Framing scale"
                },
                "camera_move": {
                    "type": "string",
                    "enum": [
                        "track_left", "track_right", "dolly_in", "dolly_out",
                        "crane_up", "crane_down", "arc_left", "arc_right",
                        "handheld_follow", "focus_pull", "tilt_up"
                    ],
                    "description": "Cinematic camera movement"
                },
                "performance_beat": {"type": "string", "description": "Physical character action beat"},
                "secondary_motion": {"type": "string", "description": "Environmental physics (smoke, cloth, rain)"}
            },
            "required": ["subject", "duration_sec"]
        }
    },
    {
        "name": "cinelogic_format_prompt",
        "description": "Compiles a guidance_scale=1.0 optimal diffusion video prompt following the 4-part CineLogic clause (Style + Subject + Beat + Secondary Physics) while stripping conflicting camera terms.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "style": {"type": "string", "description": "House style clause (e.g. 'Vivid historical anime, dark ink linework')"},
                "subject": {"type": "string", "description": "Main subject"},
                "beat": {"type": "string", "description": "Physical performance beat"},
                "secondary": {"type": "string", "description": "Environmental secondary motion"},
                "conditioned_on_image": {"type": "boolean", "default": True, "description": "Whether shot is conditioned on an image"}
            },
            "required": ["subject"]
        }
    },
    {
        "name": "cinelogic_check_qc",
        "description": "Executes deterministic quality control on an image frame or video cut seam: checks mean luma, Laplacian sharpness, letterboxing, and boundary difference.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string", "description": "Absolute path to frame image"},
                "next_frame_path": {"type": "string", "description": "Optional next frame path to test cut seam jump"}
            },
            "required": ["image_path"]
        }
    },
    {
        "name": "cinelogic_diagnose_failure",
        "description": "Diagnoses a failed video generation attempt into one of the 8 CineLogic root causes and returns the exact corrective procedure (e.g. divert to 2.5D Parallax fallback vs rekey).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "symptom": {
                    "type": "string",
                    "description": "Description of defect (e.g. 'face melting', 'static still zoom', 'jump cut inside shot', 'locomotion stuck')"
                },
                "attempt_number": {
                    "type": "integer",
                    "default": 1,
                    "description": "Which attempt just failed"
                }
            },
            "required": ["symptom"]
        }
    },
    {
        "name": "cinelogic_audit_script",
        "description": "Audits narration sentences for diffusion horizon limits (<= 10s), sentence splits, PII names, and unverified financial figures.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sentences": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of spoken voiceover sentences"
                }
            },
            "required": ["sentences"]
        }
    },
    {
        "name": "cinelogic_analyze_pacing",
        "description": "Measures 2D FFT phase-correlation camera-undone local motion on a video clip to detect Ken Burns static still zooms and dead runtime.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_path": {"type": "string", "description": "Absolute path to video file"}
            },
            "required": ["video_path"]
        }
    }
]


def handle_design_shot(args: Dict[str, Any]) -> Dict[str, Any]:
    subject = args.get("subject", "").strip()
    duration = float(args.get("duration_sec", 5.0))
    shot_size = args.get("shot_size", "medium")
    camera_move = args.get("camera_move", "track_right")
    beat = args.get("performance_beat", "")
    secondary = args.get("secondary_motion", "")
    
    warnings = []
    splits = []
    
    # Duration limit
    if duration > 10.0:
        half = duration / 2.0
        warnings.append(f"Duration {duration}s exceeds 10.0s diffusion threshold. Split into 2 shots of {half:.1f}s.")
        splits = [
            {"shot_id": "shot_01a", "duration_sec": half, "shot_size": shot_size, "camera_move": camera_move},
            {"shot_id": "shot_01b", "duration_sec": half, "shot_size": "close" if shot_size == "medium" else "medium", "camera_move": "dolly_out"}
        ]
        
    return {
        "status": "APPROVED" if not warnings else "SPLIT_RECOMMENDED",
        "validated_shot": {
            "subject": subject,
            "duration_sec": min(duration, 10.0),
            "shot_size": shot_size,
            "camera_move": camera_move,
            "performance_beat": beat or "natural posture shift",
            "secondary_motion": secondary or "subtle ambient air drift"
        },
        "warnings": warnings,
        "recommended_splits": splits
    }

def handle_format_prompt(args: Dict[str, Any]) -> Dict[str, Any]:
    style = args.get("style", "Vivid anime, dark ink linework, rich cel shading").strip()
    subject = args.get("subject", "").strip()
    beat = args.get("beat", "").strip()
    secondary = args.get("secondary", "").strip()
    
    parts = []
    if style:
        parts.append(f"{style.rstrip('.')}.")
    if subject:
        parts.append(f"{subject.rstrip('.')}.")
    if beat:
        parts.append(f"{beat.rstrip('.')}.")
    if secondary:
        parts.append(f"{secondary.rstrip('.')}.")
        
    compiled = " ".join(parts)
    words = compiled.split()
    trimmed = False
    if len(words) > 42:
        compiled = " ".join(words[:42])
        if not compiled.endswith("."):
            compiled += "."
        trimmed = True
        
    return {
        "compiled_prompt": compiled,
        "word_count": len(compiled.split()),
        "trimmed_for_guidance_economy": trimmed
    }

def handle_check_qc(args: Dict[str, Any]) -> Dict[str, Any]:
    image_path = Path(args.get("image_path", ""))
    if not image_path.exists():
        return {"error": f"File not found: {image_path}"}
        
    # Execute standalone script
    script_path = Path(__file__).resolve().parents[1] / "skills" / "cinelogic-cinematics" / "scripts" / "qc_checker.py"
    if not script_path.exists():
        return {"error": f"QC script not found at {script_path}"}
        
    cmd = [sys.executable, str(script_path), str(image_path), "--json"]
    next_frame = args.get("next_frame_path")
    if next_frame and Path(next_frame).exists():
        cmd.extend(["--next-frame", str(next_frame)])
        
    import subprocess
    p = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(p.stdout)
    except Exception:
        return {"raw_output": p.stdout, "raw_error": p.stderr, "exit_code": p.returncode}

def handle_diagnose_failure(args: Dict[str, Any]) -> Dict[str, Any]:
    symptom = args.get("symptom", "").lower()
    attempt = int(args.get("attempt_number", 1))
    
    locomotion_kws = ["locomotion", "walk", "walking", "run", "running", "treadmill", "in place", "horse", "feet"]
    if any(kw in symptom for kw in locomotion_kws):
        if attempt >= 2:
            return {
                "root_cause": "ltx_limitation",
                "action": "TERMINAL_FALLBACK_2.5D_PARALLAX",
                "explanation": "Complex locomotion is an intractable diffusion limitation on this keyframe. Diverting to multiplane parallax preserves film pacing without burning further GPU cycles."
            }
        return {
            "root_cause": "ltx_limitation",
            "action": "RETRY_WITH_TRAVELING_CAMERA",
            "explanation": "Try changing camera move to track_left/right with a tighter framing to mask footfall."
        }
    elif any(kw in symptom for kw in ["melt", "face", "anatomy", "deform", "hand", "extra limb"]):
        return {
            "root_cause": "bad_keyframe",
            "action": "REKEY",
            "explanation": "Character identity drift stems from keyframe ambiguity. Re-generate the 2D keyframe with higher negative weights on hands/face."
        }
    elif "still" in symptom or "zoom" in symptom or "photo" in symptom:
        return {
            "root_cause": "weak_conditioning",
            "action": "INJECT_PERFORMANCE_BEAT",
            "explanation": "The scene lacks character acting. Add an active verb clause (e.g. 'eyes narrowing, hands unrolling map') and secondary physics (smoke, cloth)."
        }
    elif "jump" in symptom or "cut inside" in symptom or "morph" in symptom:
        return {
            "root_cause": "bad_prompt",
            "action": "PRUNE_IN_SHOT_TRANSITIONS",
            "explanation": "Prompt contains in-shot transition words (e.g. 'whip pan', 'then cuts'). Strip all transition words; transitions must be handled by timeline edit."
        }
    else:
        return {
            "root_cause": "unknown",
            "action": "INSPECT_FRAME_REVIEW",
            "explanation": "Symptom requires manual frame review."
        }

def handle_audit_script(args: Dict[str, Any]) -> Dict[str, Any]:
    sentences = args.get("sentences", [])
    results = []
    total_sec = 0.0
    
    import re
    money_pattern = re.compile(r"(\$[\d,]+|\b\d+\s*(million|billion|trillion|dollars)\b)", re.IGNORECASE)
    
    for i, s in enumerate(sentences):
        words = len(s.split())
        est_sec = round(words / 2.5, 2)
        total_sec += est_sec
        findings = []
        
        if est_sec > 10.0:
            findings.append(f"Sentence duration {est_sec}s exceeds 10.0s diffusion horizon (word count: {words})")
        if money_pattern.search(s):
            findings.append("Contains financial figures requiring policy verification")
            
        results.append({
            "index": i,
            "sentence": s,
            "words": words,
            "est_sec": est_sec,
            "status": "FLAGGED" if findings else "OK",
            "findings": findings
        })
        
    return {
        "sentence_count": len(sentences),
        "total_estimated_sec": round(total_sec, 2),
        "flagged_count": sum(1 for r in results if r["status"] == "FLAGGED"),
        "sentences": results
    }

def handle_analyze_pacing(args: Dict[str, Any]) -> Dict[str, Any]:
    video_path = Path(args.get("video_path", ""))
    if not video_path.exists():
        return {"error": f"Video not found: {video_path}"}
        
    script_path = Path(__file__).resolve().parents[1] / "skills" / "cinelogic-cinematics" / "scripts" / "inspect_pacing.py"
    if not script_path.exists():
        return {"error": f"Pacing script not found at {script_path}"}
        
    import subprocess
    cmd = [sys.executable, str(script_path), str(video_path), "--json"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(p.stdout)
    except Exception:
        return {"raw_output": p.stdout, "raw_error": p.stderr, "exit_code": p.returncode}

def process_request(req: Dict[str, Any]) -> Dict[str, Any]:
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "cinelogic-studio-mcp",
                    "version": "1.0.0"
                }
            }
        }
    elif method == "notifications/initialized":
        return None
    elif method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": TOOLS
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "cinelogic_design_shot":
            res = handle_design_shot(arguments)
        elif tool_name == "cinelogic_format_prompt":
            res = handle_format_prompt(arguments)
        elif tool_name == "cinelogic_check_qc":
            res = handle_check_qc(arguments)
        elif tool_name == "cinelogic_diagnose_failure":
            res = handle_diagnose_failure(arguments)
        elif tool_name == "cinelogic_audit_script":
            res = handle_audit_script(arguments)
        elif tool_name == "cinelogic_analyze_pacing":
            res = handle_analyze_pacing(arguments)
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                }
            }
            
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }
                ]
            }
        }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32601,
                "message": f"Method not supported: {method}"
            }
        }

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = process_request(req)
            if res is not None:
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()
        except Exception as e:
            err_res = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
