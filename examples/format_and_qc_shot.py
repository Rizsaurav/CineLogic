#!/usr/bin/env python3
"""
CineLogic Example: Shot Prompt Formatting & Pre-Flight QC Validation
Demonstrates how to compile high-retention cinematic prompts and validate keyframes
before feeding them to generative video models.
"""

import sys
import json
from pathlib import Path

# Resolve path to skills scripts
SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "cinelogic-cinematics" / "scripts"
sys.path.insert(0, str(SKILL_DIR))

import format_prompt
import qc_checker

def main():
    print("=" * 65)
    print("🎬 CineLogic Shot Compiler & Pre-Flight QC Pipeline")
    print("=" * 65)

    # 1. Compile a production shot prompt adhering to the Guidance=1.0 syntax rule
    print("\n[Step 1] Compiling Guidance=1.0 Cinematic Shot Prompt...")
    compiled_prompt = format_prompt.compile_prompt(
        style="Dark neo-noir cyberpunk anime, 35mm anamorphic lens, high contrast rim lighting",
        subject="Cybernetic bounty hunter standing in heavy neon rain",
        beat="slowly igniting a glowing blue plasma lighter with steady metallic fingers",
        secondary="rain droplets splashing against trench coat and bokeh neon reflections"
    )
    print(f"  ✓ Compiled Prompt:  \"{compiled_prompt}\"")
    print(f"  ✓ Word Count:       {len(compiled_prompt.split())} words (Hard-capped under 42 words)")

    # 2. Run Pre-flight QC on an image fixture
    fixture_path = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "sharp_clean.png"
    if not fixture_path.exists():
        print("\n[Notice] Generating test fixture for QC demonstration...")
        from PIL import Image, ImageDraw
        fixture_path.parent.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGB", (1280, 720), (30, 30, 45))
        d = ImageDraw.Draw(img)
        d.rectangle([300, 200, 980, 520], fill=(200, 180, 80), outline=(255, 255, 255), width=4)
        img.save(fixture_path)

    print(f"\n[Step 2] Running Pre-Flight QC Gate on Keyframe: {fixture_path.name}...")
    res = qc_checker.check_image(fixture_path)

    print(f"  ✓ Mean Luminance:      {res['luma']} / 255.0 (Min: 42.0)")
    print(f"  ✓ Laplacian Sharpness: {res['sharpness']} (Min: 25.0)")
    print(f"  ✓ Letterbox Top/Bot:   {res['letterbox_top_pct']}% / {res['letterbox_bottom_pct']}% (Max: 3.0%)")
    print(f"  ✓ Passed All Gates:    {res['passed']}")
    if res["failures"]:
        print(f"  ⚠ Rejection Reasons:   {', '.join(res['failures'])}")
    else:
        print("  🚀 READY FOR DIFFUSION: Keyframe passed all deterministic gates with zero defects.")

    print("\n" + "=" * 65)
    print("✨ Pipeline Complete. Zero tokens wasted on hallucinated outputs.")
    print("=" * 65)

if __name__ == "__main__":
    main()
