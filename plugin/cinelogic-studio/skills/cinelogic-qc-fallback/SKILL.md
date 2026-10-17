---
name: cinelogic-qc-fallback
description: >-

  Executes deterministic visual QC, calculates film pacing, and deploys 2.5D parallax fallbacks.
  Use this skill when checking clips for underexposure/blur/letterboxing, evaluating camera-undone
  local motion, diagnosing failure root causes, and rendering multiplane parallax shots.
---

# CineLogic QC & Fallback Engine

This skill governs post-generation acceptance testing and mechanical fallback deployment, guaranteeing that broken generations never make it to the timeline.

---

## 1. Deterministic Quality Gates

Every generated shot must pass these exact numeric thresholds:
- **Mean Luma**: $\ge 42.0$ (prevents murky lantern shots)
- **Sharpness**: Laplacian variance $\ge 25.0$ (catches painterly blur)
- **Letterbox**: $\le 3.0\%$ consecutive black edge rows
- **Camera Wander**: Flags shots where mid-frame wanders away from start/cut points
- **Local Motion**: $\ge 4.0$ after 2D FFT phase-correlation camera zoom/pan inversion

---

## 2. The 8 Causal Root Causes

Do not blindly increment `seed += 1`. Categorize failure into one of the 8 causal states:
1. `bad_source_asset` -> Re-render clean base plate.
2. `bad_keyframe` -> Re-prompt 2D keyframe generator.
3. `bad_prompt` -> Prune in-shot transition words.
4. `wrong_visual_mode` -> Re-assert hero style anchor reference.
5. `weak_conditioning` -> Tighten framing or increase conditioning weight.
6. `ltx_limitation` -> **STOP DIFFUSION ATTEMPTS IMMEDIATELY.** Divert to 2.5D Parallax Fallback.
7. `transition_failure` -> Adjust edit boundary or insert whip pan / dissolve.
8. `none` -> Approved.

---

## 3. The 2.5D Parallax Fallback Protocol

When a shot hits `ltx_limitation`:
1. Estimate depth disparity via **Depth Anything V2 Small**.
2. Snap depth edges onto cel ink outlines using a **color-guided bilateral filter**.
3. Quantize disparity into 3–5 planes via **1D k-means**.
4. Inpaint occluded zones via **push-pull pyramid**.
5. Render continuous disparity warping with subtle $\pm 3\%$ exposure breath and floating dust motes.
6. Clears the `local_motion >= 4.0` pacing threshold without any AI deformation.
