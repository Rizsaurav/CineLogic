---
name: cinelogic-keyframes
description: >-

  Establishes visual style anchors, character sheets, location plates, and scene keyframes.
  Use this skill when defining a film's style bible, generating the hero anchor frame from text,
  maintaining character continuity across shots, and planning visual transitions.
---

# CineLogic Keyframes: Visual DNA & Consistency

This skill establishes and maintains visual cohesion across generative AI films, ensuring that characters and worlds remain consistent without identity morphing.

---

## 1. Core Principles

1. **The Hero Style Anchor (Text-Only Rule)**:
   - Every project begins with a hero style anchor frame generated **purely from text prompts**.
   - *Never restyle an existing image to create an anchor*: diffusion models return image-conditioned inputs virtually unchanged.
   - The style anchor embodies the locked house aesthetic (e.g., "Dark ink linework, saturated cel shading, 2D anime proportions").

2. **Style Profile Drafting**:
   - Establish the project world: environments, color palette (avoid washed out hues; target vibrant grades), historical accuracy rules, and character traits.
   - Pass the hero style anchor as an image-to-image reference into all subsequent keyframe generation calls (Nano Banana / Flux).

3. **Character Sheets & Location Plates**:
   - For recurring subjects, render isolated character turnaround plates and locked background plates before scene keyframes.
   - Prevents clothing and facial architecture from drifting between scenes.

4. **Cut Frame Continuity**:
   - For shots intended to continue an action, use the exact last frame of Shot A as the start keyframe of Shot B.
   - Run boundary checks: if the luma difference exceeds `45.0`, insert an edit transition (`CUT`, `WHIP_PAN`, `DISSOLVE`) instead of an unmasked join.
