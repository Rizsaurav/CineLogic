#!/usr/bin/env python3
"""CineLogic Cinematics: Standalone Pacing & Camera-Undone Local Motion Inspector

Measures:
1. Raw motion energy across frame samples
2. Local motion residual AFTER algebraically undoing camera zoom + pan via 2D FFT phase correlation
3. Flags Ken Burns static zooms (local motion < 4.0)
4. Reports dead runtime percentage
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image
import numpy as np

FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"

GEO_W, GEO_H = 320, 180
RESID_BLUR = 4
MIN_LOCAL_MOTION = 4.0
MIN_RAW_MOTION = 4.5

_WINDOWS: dict[tuple[int, int], np.ndarray] = {}

def _box(a: np.ndarray, k: int) -> np.ndarray:
    h, w = a.shape
    return a[: h // k * k, : w // k * k].reshape(h // k, k, w // k, k).mean(axis=(1, 3))

def _magnify(a: np.ndarray, m: float) -> np.ndarray:
    h, w = a.shape
    cw, ch = w / m, h / m
    x0, y0 = (w - cw) / 2, (h - ch) / 2
    im = Image.fromarray(a, "F").transform(
        (w, h), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch),
        Image.Resampling.BILINEAR
    )
    return np.asarray(im, np.float32)

def _phase_shift(a: np.ndarray, b: np.ndarray) -> tuple[int, int]:
    win = _WINDOWS.get(a.shape)
    if win is None:
        win = _WINDOWS[a.shape] = np.outer(np.hanning(a.shape[0]), np.hanning(a.shape[1])).astype(np.float32)
    fa = np.fft.fft2((a - a.mean()) * win)
    fb = np.fft.fft2((b - b.mean()) * win)
    cross = np.conj(fa) * fb
    cross /= np.abs(cross) + 1e-6
    corr = np.fft.ifft2(cross).real
    dy, dx = np.unravel_index(int(np.argmax(corr)), corr.shape)
    h, w = a.shape
    return int(dy - h if dy > h // 2 else dy), int(dx - w if dx > w // 2 else dx)

def _overlap_residual(a: np.ndarray, b: np.ndarray, dy: int, dx: int) -> float:
    h, w = a.shape
    if abs(dy) > 0.4 * h or abs(dx) > 0.4 * w:
        return float("inf")
    ya, yb = (0, dy) if dy >= 0 else (-dy, 0)
    xa, xb = (0, dx) if dx >= 0 else (-dx, 0)
    hh, ww = h - abs(dy), w - abs(dx)
    return float(np.abs(_box(a[ya:ya + hh, xa:xa + ww], RESID_BLUR)
                        - _box(b[yb:yb + hh, xb:xb + ww], RESID_BLUR)).mean())

def camera_residual(a: np.ndarray, b: np.ndarray, max_zoom: float = 1.15, steps: int = 15) -> float:
    raw = float(np.abs(_box(a, RESID_BLUR) - _box(b, RESID_BLUR)).mean())
    best = raw
    zooms = np.exp(np.linspace(0.0, np.log(max_zoom), steps))
    for i, m in enumerate(zooms):
        pairs = [(1.0, a, b)] if i == 0 else [(m, _magnify(a, m), b), (1 / m, a, _magnify(b, m))]
        for zoom, aa, bb in pairs:
            dy, dx = _phase_shift(_box(aa, 2), _box(bb, 2))
            r = _overlap_residual(aa, bb, 2 * dy, 2 * dx)
            if r < best:
                best = r
    return best

def extract_frames(video_path: Path, fps: float = 1.0) -> list[np.ndarray]:
    cmd = [
        FFMPEG, "-nostdin", "-v", "error", "-i", str(video_path),
        "-vf", f"fps={fps},scale={GEO_W}:{GEO_H}",
        "-f", "rawvideo", "-pix_fmt", "gray", "-"
    ]
    p = subprocess.run(cmd, capture_output=True, check=False)
    raw = p.stdout
    frame_size = GEO_W * GEO_H
    n_frames = len(raw) // frame_size
    frames = []
    for i in range(n_frames):
        chunk = raw[i * frame_size : (i + 1) * frame_size]
        arr = np.frombuffer(chunk, dtype=np.uint8).reshape((GEO_H, GEO_W)).astype(np.float32)
        frames.append(arr)
    return frames

def analyze_video(video_path: Path) -> dict:
    frames = extract_frames(video_path, fps=1.0)
    if len(frames) < 2:
        return {"file": str(video_path), "error": "Video duration too short (fewer than 2 frames sampled at 1 fps)"}
    
    raw_diffs = []
    local_diffs = []
    
    for i in range(len(frames) - 1):
        raw_diff = float(np.abs(frames[i + 1] - frames[i]).mean())
        raw_diffs.append(raw_diff)
        
        local_res = camera_residual(frames[i], frames[i + 1])
        local_diffs.append(local_res)
        
    mean_raw = float(np.mean(raw_diffs))
    mean_local = float(np.mean(local_diffs))
    
    is_zoom_only = mean_local < MIN_LOCAL_MOTION
    is_freeze = mean_raw < MIN_RAW_MOTION
    is_dead = is_zoom_only or is_freeze
    
    return {
        "file": str(video_path),
        "sampled_seconds": len(frames),
        "mean_raw_motion": round(mean_raw, 2),
        "mean_local_motion": round(mean_local, 2),
        "is_zoom_only_still": is_zoom_only,
        "is_freeze": is_freeze,
        "is_dead_runtime": is_dead,
        "verdict": "DEAD_STILL (Ken Burns zoom)" if is_zoom_only else ("FREEZE" if is_freeze else "ACTIVE_CINEMATIC")
    }

def main():
    parser = argparse.ArgumentParser(description="Analyze video pacing and camera-undone local motion.")
    parser.add_argument("video", type=Path, help="Path to video file (.mp4, .mov, etc.)")
    parser.add_argument("--json", action="store_true", help="Output JSON results")
    args = parser.parse_args()
    
    if not args.video.exists():
        print(f"Error: {args.video} not found", file=sys.stderr)
        sys.exit(1)
        
    res = analyze_video(args.video)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"=== Pacing Analysis: {args.video.name} ===")
        print(f"  Sampled Seconds:    {res.get('sampled_seconds', 0)}s")
        print(f"  Raw Motion Energy:  {res.get('mean_raw_motion')} (gate: >= {MIN_RAW_MOTION})")
        print(f"  Local Motion:       {res.get('mean_local_motion')} (gate: >= {MIN_LOCAL_MOTION})")
        print(f"  Verdict:            {res.get('verdict')}")
        if res.get("is_dead_runtime"):
            print("  [!] WARNING: This clip reads as a still photo with camera zoom. Consider 2.5D Parallax fallback.")
    
    sys.exit(0 if not res.get("is_dead_runtime") else 1)

if __name__ == "__main__":
    main()
