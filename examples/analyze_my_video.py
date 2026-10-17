#!/usr/bin/env python3
"""CineLogic Example: Video Pacing & Ken Burns Still Detector

Decouples camera zoom from internal character motion using 2D Fast Fourier
Transform (FFT) phase correlation. Detects whether a video is clinically dead
despite changing pixels.

Usage:
    python3 examples/analyze_my_video.py [video_path]
"""

from __future__ import annotations

import sys
from pathlib import Path

import importlib.util

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

pacing_script = ROOT / "skills" / "cinelogic-cinematics" / "scripts" / "inspect_pacing.py"
spec = importlib.util.spec_from_file_location("inspect_pacing", pacing_script)
pacing_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pacing_mod)
analyze_video = pacing_mod.analyze_video


def main():
    if len(sys.argv) > 1:
        video_path = Path(sys.argv[1])
    else:
        video_path = ROOT / "tests" / "fixtures" / "ken_burns_zoom.mp4"
        
    print(f"🔍 CineLogic Fourier Pacing Inspector")
    print(f"  Target Video: {video_path}\n")
    
    if not video_path.exists():
        print(f"❌ Video not found: {video_path}")
        sys.exit(1)
        
    res = analyze_video(video_path)
    
    print(f"📊 Measurement Results:")
    print(f"  • Sampled Timeline:    {res.get('sampled_seconds', 0)} seconds")
    print(f"  • Raw Motion Energy:   {res.get('mean_raw_motion')} (Naive difference)")
    print(f"  • Local Motion (FFT):  {res.get('mean_local_motion')} (Camera-undone residual, threshold >= 4.0)")
    print(f"  • Pacing Verdict:      {res.get('verdict')}\n")
    
    if res.get("is_dead_runtime"):
        print("🚨 AUDIENCE RETENTION ALERT:")
        print("  This shot is a Ken Burns still zoom. The camera is moving, but the subjects")
        print("  are rigid 2D cardboard cutouts. Viewers will drop off. Deploy 2.5D Parallax fallback.")
    else:
        print("✅ CINEMATIC PASS:")
        print("  Genuine non-rigid character acting or fluid physics detected.")

if __name__ == "__main__":
    main()
