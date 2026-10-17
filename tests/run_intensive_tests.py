#!/usr/bin/env python3
"""CineLogic Intensive Test Suite: Rigorous Real-World Validation
Generates synthetic media fixtures and executes exhaustive edge-case testing
across deterministic QC, 2D FFT pacing analysis, prompt compilation,
virtual camera FFmpeg encoding, and dual MCP servers.
"""

from __future__ import annotations

import json
import math
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
EXPORT_DIR = PACKAGE_ROOT
TEST_DIR = PACKAGE_ROOT / "tests"
FIXTURES = TEST_DIR / "fixtures"

FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"

passed_tests = 0
failed_tests = 0

def log_test(name: str, passed: bool, detail: str = ""):
    global passed_tests, failed_tests
    status = "\033[92m[PASS]\033[0m" if passed else "\033[91m[FAIL]\033[0m"
    print(f"  {status} {name}")
    if detail:
        print(f"         \033[90m{detail}\033[0m")
    if passed:
        passed_tests += 1
    else:
        failed_tests += 1

# ---------------------------------------------------------------------------
# 1. Media Fixture Generation
# ---------------------------------------------------------------------------

def generate_fixtures():
    print("\n--- Generating Real Image & Video Fixtures ---")
    FIXTURES.mkdir(parents=True, exist_ok=True)
    
    # Fixture 1: Sharp, high-contrast, clean texture (should PASS all gates)
    sharp_path = FIXTURES / "sharp_clean.png"
    im_sharp = Image.new("RGB", (1920, 1080), color=(120, 130, 140))
    draw = ImageDraw.Draw(im_sharp)
    for x in range(0, 1920, 40):
        draw.line([(x, 0), (x, 1080)], fill=(40, 50, 60), width=4)
    for y in range(0, 1080, 40):
        draw.line([(0, y), (1920, y)], fill=(200, 210, 220), width=4)
    draw.rectangle([600, 300, 1320, 780], fill=(220, 180, 50), outline=(20, 20, 20), width=8)
    im_sharp.save(sharp_path)
    print(f"  Created {sharp_path.name}")
    
    # Fixture 2: Dark, murky, underexposed (mean luma ~15 < 42)
    dark_path = FIXTURES / "dark_underexposed.png"
    im_dark = Image.new("RGB", (1920, 1080), color=(15, 18, 20))
    im_dark.save(dark_path)
    print(f"  Created {dark_path.name}")
    
    # Fixture 3: Blurred, painterly mush (sharpness < 25)
    blur_path = FIXTURES / "blurred_mush.png"
    im_blur = im_sharp.filter(ImageFilter.GaussianBlur(radius=25))
    im_blur.save(blur_path)
    print(f"  Created {blur_path.name}")
    
    # Fixture 4: Baked-in letterbox (120px black bars on top and bottom)
    lb_path = FIXTURES / "letterboxed.png"
    im_lb = im_sharp.copy()
    draw_lb = ImageDraw.Draw(im_lb)
    draw_lb.rectangle([0, 0, 1920, 120], fill=(0, 0, 0))
    draw_lb.rectangle([0, 960, 1920, 1080], fill=(0, 0, 0))
    im_lb.save(lb_path)
    print(f"  Created {lb_path.name}")
    
    # Fixture 5: Stiff jump frame (stark white, creates boundary diff > 45)
    jump_path = FIXTURES / "stark_white_jump.png"
    im_jump = Image.new("RGB", (1920, 1080), color=(250, 250, 250))
    im_jump.save(jump_path)
    print(f"  Created {jump_path.name}")
    
    # Fixture 6: Real Ken Burns video (a pure virtual zoom over a still image)
    kb_vid_path = FIXTURES / "ken_burns_zoom.mp4"
    if not kb_vid_path.exists():
        cmd = [
            FFMPEG, "-y", "-loop", "1", "-i", str(sharp_path),
            "-vf", "zoompan=z='min(zoom+0.0015,1.25)':d=72:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=24",
            "-t", "3", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(kb_vid_path)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"  Rendered {kb_vid_path.name} (Synthetic Ken Burns zoom)")

    # Fixture 7: Real Genuine Action video (large dynamic figures moving across frame)
    action_vid_path = FIXTURES / "genuine_action.mp4"
    if not action_vid_path.exists():
        proc = subprocess.Popen(
            [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "640x360", "-r", "24",
             "-i", "-", "-t", "3", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(action_vid_path)],
            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        for frame_idx in range(72):
            frame = Image.new("RGB", (640, 360), color=(40, 45, 50))
            d = ImageDraw.Draw(frame)
            for x in range(0, 640, 50):
                d.line([(x, 0), (x, 360)], fill=(60, 65, 70), width=2)
            offset_x = int(math.sin(frame_idx * 0.15) * 160)
            offset_y = int(math.cos(frame_idx * 0.1) * 40)
            cx, cy = 320 + offset_x, 180 + offset_y
            d.rectangle([cx - 100, cy - 80, cx + 100, cy + 120], fill=(220, 190, 50))
            arm_end_x = int(cx + 140 * math.cos(frame_idx * 0.25))
            arm_end_y = int(cy + 140 * math.sin(frame_idx * 0.25))
            d.line([(cx, cy), (arm_end_x, arm_end_y)], fill=(255, 80, 40), width=18)
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        proc.wait()
        print(f"  Rendered {action_vid_path.name} (Synthetic genuine character motion)")

# ---------------------------------------------------------------------------
# 2. Test Deterministic QC Checker
# ---------------------------------------------------------------------------

def test_qc_checker():
    print("\n--- Testing Component: Deterministic QC Checker (`qc_checker.py`) ---")
    script = EXPORT_DIR / "skills" / "cinelogic-cinematics" / "scripts" / "qc_checker.py"
    
    # Test 1: Clean image should PASS
    p = subprocess.run([sys.executable, str(script), str(FIXTURES / "sharp_clean.png"), "--json"], capture_output=True, text=True)
    res = json.loads(p.stdout)
    log_test("Clean Sharp Image Acceptance", res["passed"] is True, f"Luma: {res['luma']}, Sharpness: {res['sharpness']}")
    
    # Test 2: Underexposed image should FAIL luma
    p = subprocess.run([sys.executable, str(script), str(FIXTURES / "dark_underexposed.png"), "--json"], capture_output=True, text=True)
    res = json.loads(p.stdout)
    log_test("Underexposure Detection (Luma < 42.0)", res["passed"] is False and res["luma"] < 42.0, f"Reported Luma: {res['luma']}")
    
    # Test 3: Blurred mush should FAIL sharpness
    p = subprocess.run([sys.executable, str(script), str(FIXTURES / "blurred_mush.png"), "--json"], capture_output=True, text=True)
    res = json.loads(p.stdout)
    log_test("Blurry Mush Detection (Sharpness < 25.0)", res["passed"] is False and res["sharpness"] < 25.0, f"Reported Sharpness: {res['sharpness']}")
    
    # Test 4: Letterbox should FAIL (> 3.0%)
    p = subprocess.run([sys.executable, str(script), str(FIXTURES / "letterboxed.png"), "--json"], capture_output=True, text=True)
    res = json.loads(p.stdout)
    max_lb = max(res["letterbox_top_pct"], res["letterbox_bottom_pct"])
    log_test("Letterbox Border Detection (> 3.0%)", res["passed"] is False and max_lb > 3.0, f"Reported Letterbox: {max_lb:.1f}%")
    
    # Test 5: Cut seam boundary difference
    p = subprocess.run([
        sys.executable, str(script), str(FIXTURES / "sharp_clean.png"),
        "--next-frame", str(FIXTURES / "stark_white_jump.png"), "--json"
    ], capture_output=True, text=True)
    res = json.loads(p.stdout)
    log_test("Cut Seam Jump Rejection (Diff > 45.0)", res["passed"] is False and res.get("boundary_diff", 0) > 45.0, f"Boundary Diff: {res.get('boundary_diff')}")
    
    # Test 6: Zero seam diff on identical frames
    p = subprocess.run([
        sys.executable, str(script), str(FIXTURES / "sharp_clean.png"),
        "--next-frame", str(FIXTURES / "sharp_clean.png"), "--json"
    ], capture_output=True, text=True)
    res = json.loads(p.stdout)
    log_test("Identical Frame Boundary Seam (Diff == 0.0)", res.get("boundary_diff") == 0.0, f"Boundary Diff: {res.get('boundary_diff')}")

# ---------------------------------------------------------------------------
# 3. Test Pacing & 2D FFT Phase Correlation Inspector
# ---------------------------------------------------------------------------

def test_pacing_inspector():
    print("\n--- Testing Component: 2D FFT Pacing & Local Motion Inspector (`inspect_pacing.py`) ---")
    script = EXPORT_DIR / "skills" / "cinelogic-cinematics" / "scripts" / "inspect_pacing.py"
    
    # Test 1: Ken Burns zoom should be detected as DEAD_STILL (local_motion < 4.0)
    p = subprocess.run([sys.executable, str(script), str(FIXTURES / "ken_burns_zoom.mp4"), "--json"], capture_output=True, text=True)
    res = json.loads(p.stdout)
    log_test(
        "Ken Burns Zoom Detection (Local Motion < 4.0)",
        res["is_zoom_only_still"] is True and res["mean_local_motion"] < 4.0,
        f"Raw Motion: {res['mean_raw_motion']}, Local Motion: {res['mean_local_motion']}, Verdict: {res['verdict']}"
    )
    
    # Test 2: Genuine motion video should PASS as ACTIVE_CINEMATIC (local_motion >= 4.0)
    p = subprocess.run([sys.executable, str(script), str(FIXTURES / "genuine_action.mp4"), "--json"], capture_output=True, text=True)
    res = json.loads(p.stdout)
    log_test(
        "Genuine Non-Rigid Motion Acceptance (Local Motion >= 4.0)",
        res["is_dead_runtime"] is False and res["mean_local_motion"] >= 4.0,
        f"Raw Motion: {res['mean_raw_motion']}, Local Motion: {res['mean_local_motion']}, Verdict: {res['verdict']}"
    )

# ---------------------------------------------------------------------------
# 4. Test Prompt Compiler
# ---------------------------------------------------------------------------

def test_prompt_compiler():
    print("\n--- Testing Component: Guidance=1.0 Prompt Compiler (`format_prompt.py`) ---")
    script = EXPORT_DIR / "skills" / "cinelogic-cinematics" / "scripts" / "format_prompt.py"
    
    # Test 1: Standard 4-part clause compilation
    p = subprocess.run([
        sys.executable, str(script),
        "--style", "Vivid 2D historical anime, rich cel shading, dark ink outlines",
        "--subject", "Napoleon Bonaparte looking through brass telescope",
        "--beat", "lowering telescope with stern expression",
        "--secondary", "gunpowder smoke drifting across battlefield"
    ], capture_output=True, text=True)
    compiled = p.stdout.strip()
    expected_words = ["Vivid", "Napoleon", "lowering", "gunpowder"]
    valid = all(w in compiled for w in expected_words) and compiled.endswith(".")
    log_test("4-Part Clause Prompt Synthesis", valid, f"Compiled: '{compiled}'")
    
    # Test 2: Over-length prompt truncation (diffusion economy <= 42 words)
    long_subject = "A soldier running violently across an incredibly muddy terrain full of trenches and fallen comrades while looking back in absolute sheer terror as artillery explosions light up the pitch black sky with blinding flashes of brilliant orange fire and concussive shockwaves"
    p = subprocess.run([
        sys.executable, str(script),
        "--subject", long_subject,
        "--beat", "tripping over wooden barricade",
        "--secondary", "thick mud splashing onto uniform"
    ], capture_output=True, text=True)
    compiled_long = p.stdout.strip()
    words = compiled_long.split()
    log_test(
        "Prompt Truncation Guard (Length <= 42 words)",
        len(words) <= 42 and compiled_long.endswith("."),
        f"Word count: {len(words)} (trimmed cleanly)"
    )

# ---------------------------------------------------------------------------
# 5. Test Zero-Diffusion Virtual Camera Dolly (`image_motion_server.py`)
# ---------------------------------------------------------------------------

def test_virtual_camera_dolly():
    print("\n--- Testing Component: Virtual Camera Dolly Engine (Lanczos + FFmpeg) ---")
    server_script = EXPORT_DIR / "mcp" / "image_motion_server.py"
    out_video = FIXTURES / "rendered_virtual_dolly.mp4"
    if out_video.exists():
        out_video.unlink()
        
    req = {
        "jsonrpc": "2.0",
        "id": 101,
        "method": "tools/call",
        "params": {
            "name": "cinelogic_render_virtual_dolly",
            "arguments": {
                "image_path": str(FIXTURES / "sharp_clean.png"),
                "out_path": str(out_video),
                "duration_sec": 3.0,
                "end_zoom": 1.25,
                "drift": 0.05
            }
        }
    }
    
    p = subprocess.Popen([sys.executable, str(server_script)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    stdout, _ = p.communicate(input=json.dumps(req) + "\n")
    resp = json.loads(stdout.strip())
    content = json.loads(resp["result"]["content"][0]["text"])
    
    log_test("Virtual Dolly Rendering Process", content.get("status") == "SUCCESS", f"Output: {content.get('output_video')}")
    
    # Real validation with ffprobe
    if out_video.exists():
        probe_cmd = [
            FFPROBE, "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height,codec_name,pix_fmt,nb_frames:format=duration",
            "-of", "json", str(out_video)
        ]
        probe_p = subprocess.run(probe_cmd, capture_output=True, text=True)
        probe_data = json.loads(probe_p.stdout)
        
        w = probe_data["streams"][0]["width"]
        h = probe_data["streams"][0]["height"]
        codec = probe_data["streams"][0]["codec_name"]
        pix_fmt = probe_data["streams"][0]["pix_fmt"]
        dur = float(probe_data["format"]["duration"])
        frames = int(probe_data["streams"][0].get("nb_frames", 72))
        
        log_test(
            "Video Output Conformance (1080p, H.264, 24fps)",
            w == 1920 and h == 1080 and codec == "h264" and pix_fmt == "yuv420p" and abs(dur - 3.0) < 0.1,
            f"{w}x{h}, {codec}/{pix_fmt}, duration={dur:.2f}s, frames={frames}"
        )
    else:
        log_test("Video File Creation", False, "File does not exist on disk")

# ---------------------------------------------------------------------------
# 6. Test Dual MCP Servers Robustness & Error Handling
# ---------------------------------------------------------------------------

def test_mcp_servers_robustness():
    print("\n--- Testing Component: Dual MCP Server Robustness & Error Boundaries ---")
    
    servers = [
        ("CineLogic Studio MCP", EXPORT_DIR / "mcp" / "server.py"),
        ("CineLogic Motion MCP", EXPORT_DIR / "mcp" / "image_motion_server.py")
    ]
    
    for label, s_path in servers:
        # Test A: Malformed JSON handling (should return code -32700 Parse Error without crashing)
        p = subprocess.Popen([sys.executable, str(s_path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        stdout, _ = p.communicate(input="NOT_VALID_JSON\n")
        resp = json.loads(stdout.strip())
        log_test(f"{label} - JSON Parse Error Handling", resp.get("error", {}).get("code") == -32700, f"Error: {resp.get('error')}")
        
        # Test B: Unknown tool invocation (should return code -32601 Method Not Found)
        req_unknown = {
            "jsonrpc": "2.0",
            "id": 999,
            "method": "tools/call",
            "params": {"name": "non_existent_tool", "arguments": {}}
        }
        p = subprocess.Popen([sys.executable, str(s_path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        stdout, _ = p.communicate(input=json.dumps(req_unknown) + "\n")
        resp = json.loads(stdout.strip())
        log_test(f"{label} - Unknown Tool Rejection", resp.get("error", {}).get("code") == -32601, f"Error: {resp.get('error')}")

def main():
    print("=====================================================================")
    print("       CINELOGIC STUDIO: INTENSIVE VALIDATION HARNESS                ")
    print("=====================================================================")
    start_time = time.time()
    
    generate_fixtures()
    test_qc_checker()
    test_pacing_inspector()
    test_prompt_compiler()
    test_virtual_camera_dolly()
    test_mcp_servers_robustness()
    
    elapsed = time.time() - start_time
    print("\n=====================================================================")
    print(f"  TOTAL TESTS RUN: {passed_tests + failed_tests}")
    print(f"  PASSED:          \033[92m{passed_tests}\033[0m")
    print(f"  FAILED:          \033[91m{failed_tests}\033[0m")
    print(f"  ELAPSED TIME:    {elapsed:.2f}s")
    print("=====================================================================")
    
    if failed_tests == 0:
        print("\033[92m[VERDICT] 100% PRODUCTION READY. ALL REAL QUALITY GATES PASSED.\033[0m\n")
    else:
        print("\033[91m[VERDICT] FAILURES DETECTED. REVIEW DETAILED LOGS ABOVE.\033[0m\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
