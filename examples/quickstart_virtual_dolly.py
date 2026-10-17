#!/usr/bin/env python3
"""CineLogic Example: Quickstart Virtual Camera Dolly

Renders a broadcast-grade 1080p virtual push-in with organic lateral drift over an image
using subpixel Lanczos interpolation and FFmpeg rawvideo pipes (Zero-GPU required).

Usage:
    python3 examples/quickstart_virtual_dolly.py [input_image] [output_video]
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mcp.image_motion_server import handle_render_virtual_dolly

def main():
    if len(sys.argv) > 2:
        img_path = Path(sys.argv[1])
        out_path = Path(sys.argv[2])
    else:
        img_path = ROOT / "tests" / "fixtures" / "sharp_clean.png"
        out_path = ROOT / "tests" / "fixtures" / "quickstart_demo.mp4"
        
    print(f"🎬 CineLogic Virtual Camera Dolly Engine")
    print(f"  Input Image:   {img_path}")
    print(f"  Output Video:  {out_path}")
    print(f"  Specs:         1080p @ 24fps, Lanczos Subpixel Easing + 4% Lateral Drift\n")
    
    res = handle_render_virtual_dolly({
        "image_path": str(img_path),
        "out_path": str(out_path),
        "duration_sec": 4.0,
        "end_zoom": 1.22,
        "drift": 0.04
    })
    
    if res.get("status") == "SUCCESS":
        print(f"✨ Successfully rendered in {res['duration_sec']}s ({res['frames_rendered']} frames)!")
        print(f"  Saved to: {res['output_video']}")
    else:
        print(f"❌ Error: {res.get('error')}")

if __name__ == "__main__":
    main()
