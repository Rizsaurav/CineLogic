---
name: cinelogic-director
description: >-
  Directs shot cinematography, camera motion, and acting beats for AI video generation.
  Use this skill when converting script sentences into visual shot plans, selecting camera moves,
  enforcing variety constraints (<=25% push-ins, no 3 identical moves), and compiling
  guidance=1.0 diffusion prompts.
---

# CineLogic Director: Cinematic Motion & Camera Design

This skill enforces professional cinematic grammar across AI video sequences, preventing monotonous camera movements and prompt pollution.

---

## 1. Director's Combinatorial Invariants

1. **The 25% Push-In Ceiling**:
   Push-in shots (`dolly_in`, zoom-in) must never exceed 25% of all shots in a project.

2. **The Rule of Three**:
   - Never allow the same camera move family (`track`, `dolly`, `crane`, `arc`) to appear 3 times consecutively.
   - Never allow the same shot size (`extreme_wide`, `wide`, `medium`, `close`, `extreme_close`) to appear 3 times consecutively.

3. **Mandatory Performance Beats**:
   Every shot depicting human characters must feature an active physical verb ("reloading musket", "unfurling parchment", "head snapping toward noise").

4. **Environmental Secondary Motion**:
   Every shot must contain environmental physics ("lantern soot drifting", "wind tearing wool cloak", "rain puddles splashing").

5. **Guidance Scale = 1.0 Prompt Economy**:
   Never include camera move keywords in keyframe-conditioned diffusion prompts. Construct prompts strictly as:
   $$\text{Prompt} = [\text{Style}] + [\text{Subject}] + [\text{Performance Beat}] + [\text{Secondary Motion}]$$

---

## 2. Standard Workflow

1. For each script sentence, assign a shot size from `SIZE_ORDER`.
2. Select an approved camera move (`track_left/right`, `dolly_in/out`, `crane_up/down`, `arc_left/right`, `handheld_follow`).
3. Check project history to ensure the 25% push-in ceiling and Rule of Three are satisfied.
4. Compile the prompt via MCP tool `cinelogic_format_prompt`.

