#!/usr/bin/env python3
"""CineLogic Cinematics: Standalone Deterministic QC Checker

Performs cheap, mathematical quality control on frames and video clips:
- Exposure check (Mean Luma >= 42.0)
- Sharpness check via Laplacian Variance (Sharpness >= 25.0)
- Letterbox detection (Consecutive black borders <= 3.0%)
- Continuity boundary seam difference (Max Luma Diff <= 45.0)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from PIL import Image
import numpy as np

MIN_MEAN_LUMA = 42.0
MIN_SHARPNESS = 25.0
MAX_LETTERBOX_PCT = 3.0
MAX_BOUNDARY_DIFF = 45.0

def load_gray(image_path: Path, width: int = 640) -> np.ndarray:
    with Image.open(image_path) as im:
        im = im.convert("L")
        w, h = im.size
        new_h = int(h * width / w)
        im = im.resize((width, new_h))
        return np.asarray(im, dtype=np.float32)

def compute_luma(gray: np.ndarray) -> float:
    return float(gray.mean())

def compute_sharpness(gray: np.ndarray) -> float:
    # 2D Laplacian convolution
    lap = (
        gray[1:-1, :-2] + gray[1:-1, 2:] + gray[:-2, 1:-1] + gray[2:, 1:-1]
        - 4 * gray[1:-1, 1:-1]
    )
    return float(lap.var())

def compute_letterbox(gray: np.ndarray, dark_threshold: float = 12.0) -> tuple[float, float]:
    rows = gray.mean(axis=1)
    h = len(rows)
    top = next((i for i, v in enumerate(rows) if v > dark_threshold), h)
    bottom = next((i for i, v in enumerate(rows[::-1]) if v > dark_threshold), h)
    return 100.0 * top / h, 100.0 * bottom / h

def compute_boundary_diff(frame_a_path: Path, frame_b_path: Path) -> float:
    a = load_gray(frame_a_path, width=160)
    b = load_gray(frame_b_path, width=160)
    h = min(a.shape[0], b.shape[0])
    return float(np.abs(a[:h] - b[:h]).mean())

def check_image(image_path: Path) -> dict:
    gray = load_gray(image_path)
    luma = compute_luma(gray)
    sharpness = compute_sharpness(gray)
    top_lb, bottom_lb = compute_letterbox(gray)
    max_lb = max(top_lb, bottom_lb)
    
    failures = []
    if luma < MIN_MEAN_LUMA:
        failures.append(f"Underexposed: mean luma {luma:.1f} < {MIN_MEAN_LUMA}")
    if sharpness < MIN_SHARPNESS:
        failures.append(f"Blury / mush: sharpness {sharpness:.1f} < {MIN_SHARPNESS}")
    if max_lb > MAX_LETTERBOX_PCT:
        failures.append(f"Baked-in letterbox: {max_lb:.1f}% > {MAX_LETTERBOX_PCT}%")
        
    return {
        "file": str(image_path),
        "passed": len(failures) == 0,
        "luma": round(luma, 2),
        "sharpness": round(sharpness, 2),
        "letterbox_top_pct": round(top_lb, 2),
        "letterbox_bottom_pct": round(bottom_lb, 2),
        "failures": failures
    }

def main():
    parser = argparse.ArgumentParser(description="Deterministic QC check for frames and image boundaries.")
    parser.add_argument("image", type=Path, help="Path to image or keyframe")
    parser.add_argument("--next-frame", type=Path, default=None, help="Optional next frame to check cut seam boundary difference")
    parser.add_argument("--json", action="store_true", help="Output raw JSON results")
    
    args = parser.parse_args()
    if not args.image.exists():
        print(f"Error: {args.image} does not exist", file=sys.stderr)
        sys.exit(1)
        
    res = check_image(args.image)
    
    if args.next_frame and args.next_frame.exists():
        diff = compute_boundary_diff(args.image, args.next_frame)
        res["boundary_diff"] = round(diff, 2)
        if diff > MAX_BOUNDARY_DIFF:
            res["failures"].append(f"Discontinuous cut seam: luma diff {diff:.1f} > {MAX_BOUNDARY_DIFF}")
            res["passed"] = False
            
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        status = "PASS" if res["passed"] else "FAIL"
        print(f"[{status}] {args.image.name} - Luma: {res['luma']}, Sharpness: {res['sharpness']}, Letterbox: {max(res['letterbox_top_pct'], res['letterbox_bottom_pct'])}%")
        if res.get("boundary_diff") is not None:
            print(f"       Boundary Seam Diff: {res['boundary_diff']}")
        if res["failures"]:
            print("       Issues:")
            for f in res["failures"]:
                print(f"         - {f}")
                
    sys.exit(0 if res["passed"] else 1)

if __name__ == "__main__":
    main()
