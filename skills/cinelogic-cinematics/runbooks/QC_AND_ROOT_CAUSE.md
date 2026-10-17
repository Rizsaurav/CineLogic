# Visual QC & Root-Cause Attribution Runbook

Quality control in generative video fails when it relies solely on probabilistic LLM judgment or naive pixel diffs. CineLogic separates QC into a two-tier architecture: **Deterministic Metric Gates** followed by **Structured Causal Attribution**.

---

## 1. Deterministic Signal Processing Gates

Run these cheap, exact numeric filters on every generated clip before invoking any LLM or VLM:

| Metric | Threshold | Method | What It Catches |
|---|---|---|---|
| **Mean Luma** | `< 42.0` | Grayscale average across frames | Murky, underexposed, or black lantern shots |
| **Sharpness** | `< 25.0` | Laplacian variance on grayscale | Painterly mush, out-of-focus diffusion blur |
| **Letterbox** | `> 3.0%` | Consecutive near-black rows at edges | Accidental baked-in cinematic black bars |
| **Camera Wander** | Triggered | Mid-frame distance > 60.0 & start/end < 30.0 | Out-and-back jump cuts within a single shot |
| **Boundary Jump** | `> 45.0` | Luma diff between cut frame & next first frame | Discontinuous continuity cuts |
| **Motion Energy** | `< 4.5` | Sampling at 0.5s intervals | Complete frame freeze |

---

## 2. The 8 Causal Root-Cause Classifications

When a shot fails either a deterministic gate or the VLM critic, do **NOT** just change the random seed. Categorize the failure into one of eight root causes to trigger the appropriate mechanical remedy:

### 1. `bad_source_asset`
- **Symptom**: Historical map, flag, or object has modern digital artifacts or hallucinated text.
- **Remedy**: Re-render or fetch the base historical plate; do not touch diffusion parameters.

### 2. `bad_keyframe`
- **Symptom**: Anatomy defects, multiple heads, deformed hands, or wrong character clothing visible in frame 0.
- **Remedy**: Discard the keyframe. Re-prompt the 2D keyframe generator with higher negative prompts or fresh composition.

### 3. `bad_prompt`
- **Symptom**: Scene geometry explodes mid-shot (e.g., a character transforms into a horse).
- **Remedy**: The prompt contained conflicting verbs or in-shot transition words ("cuts to", "explodes into"). Prune conflicting action clauses.

### 4. `wrong_visual_mode`
- **Symptom**: Shot requested photorealism when the project style is cel-shaded anime, or requested 3D render when 2D was targeted.
- **Remedy**: Re-assert the style anchor reference image in the keyframing pass.

### 5. `weak_conditioning`
- **Symptom**: Video output drifts away from the keyframe character's appearance by second 2.
- **Remedy**: Increase keyframe conditioning weight or crop keyframe to tighter framing.

### 6. `ltx_limitation`
- **Symptom**: Complex locomotion (e.g., horse gallop, multi-character wrestling) that diffusion models consistently fail across 2+ attempts.
- **Remedy**: **IMMEDIATELY STOP DIFFUSION ATTEMPTS.** Divert the shot to the 2.5D Parallax Fallback Engine (`parallax.py`).

### 7. `transition_failure`
- **Symptom**: Hard seam jump between Shot A and Shot B.
- **Remedy**: Extract the exact last frame of Shot A to serve as the start frame for Shot B, or replace hard cut with an edit transition (`WHIP_PAN` or `DISSOLVE`).

### 8. `none`
- **Symptom**: Clip passed all criteria cleanly.
- **Remedy**: Approve and commit clip to final timeline.
