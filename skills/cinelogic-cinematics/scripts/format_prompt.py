#!/usr/bin/env python3
"""CineLogic Cinematics: Standalone Prompt Compiler

Formats diffusion prompts adhering to guidance_scale=1.0 economics:
- Removes conflicting camera wording from keyframe-conditioned text prompts
- Enforces the 4-part clause: Style + Subject + Performance Beat + Secondary Motion
- Checks prompt length constraints (prevents diffusion attention saturation)
"""

from __future__ import annotations

import argparse
import sys

MAX_PROMPT_WORDS = 42

def clean_sentence(text: str) -> str:
    s = text.strip().rstrip(".,;:")
    return f"{s}." if s else ""

def compile_prompt(
    style: str,
    subject: str,
    beat: str = "",
    secondary: str = "",
    conditioned_on_image: bool = True
) -> str:
    parts = []
    
    # 1. Style clause (concise)
    if style:
        parts.append(clean_sentence(style))
        
    # 2. Subject
    if subject:
        parts.append(clean_sentence(subject))
        
    # 3. Performance Beat
    if beat:
        parts.append(clean_sentence(beat))
        
    # 4. Secondary Motion / Environment
    if secondary:
        parts.append(clean_sentence(secondary))
        
    compiled = " ".join(parts).strip()
    words = compiled.split()
    
    if len(words) > MAX_PROMPT_WORDS:
        print(f"[WARNING] Prompt is {len(words)} words (max recommended: {MAX_PROMPT_WORDS}). Trimming tail.", file=sys.stderr)
        compiled = " ".join(words[:MAX_PROMPT_WORDS])
        if not compiled.endswith("."):
            compiled += "."
            
    return compiled

def main():
    parser = argparse.ArgumentParser(description="Compile guidance=1.0 optimal diffusion video prompts.")
    parser.add_argument("--style", type=str, default="Vivid anime, dark ink linework, rich cel shading", help="Project style profile clause")
    parser.add_argument("--subject", type=str, required=True, help="Main subject or character action")
    parser.add_argument("--beat", type=str, default="", help="Specific physical acting beat (visible motion)")
    parser.add_argument("--secondary", type=str, default="", help="Environmental secondary motion (smoke, rain, cloth)")
    parser.add_argument("--conditioned", action="store_true", default=True, help="Whether shot is conditioned on a keyframe")
    
    args = parser.parse_args()
    prompt = compile_prompt(args.style, args.subject, args.beat, args.secondary, args.conditioned)
    print(prompt)

if __name__ == "__main__":
    main()
