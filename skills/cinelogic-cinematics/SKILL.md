---
name: cinelogic-cinematics
description: >-
  Automates professional AI filmmaking workflows based on the CineLogic engine.
  Use this skill when planning video scenes, structuring cinematic camera movement,
  compiling guidance-optimized prompts, analyzing video pacing to prevent dead runtime,
  running deterministic visual QC, or generating 2.5D multiplane parallax fallbacks.
---

# CineLogic Cinematics: Professional AI Video Director & Pipeline Engine

This skill encapsulates the battle-hardened heuristics, camera vocabularies, motion grammars, and quality control architectures developed in CineLogic. It transforms unpredictable text-to-video / image-to-video diffusion into a deterministic, high-retention cinematic manufacturing line.

---

## 1. Core Principles (The CineLogic Doctrines)

1. **The Pacing Rule (`local_motion >= 4.0`)**:
   Never trust raw pixel movement. An AI video model applying a slow zoom over a static 2D drawing will pass naive motion thresholds while causing viewer churn. Genuine life requires non-rigid residual movement (characters acting, hair/cloth physics, fluid dynamics, lighting shifts).

2. **The Prompt Economy Doctrine (Guidance Scale = 1.0)**:
   In distilled and high-throughput video pipelines operating at guidance scale 1.0, negative prompts have zero mathematical effect. The conditioning keyframe carries 100% of the style. **Never pollute video generation prompts with redundant style descriptions or camera move keywords when keyframe-conditioned**—doing so forces the model into mid-clip scene morphs and jump cuts.

3. **The 25% Push-In Constraint & Rule of Three**:
   - Push-in / zoom-in shots must never exceed 25% of a film's total shots.
   - Never allow the same camera move family (track, dolly, crane, arc) or the same shot size (extreme wide, wide, medium, close, extreme close) to occur 3 times consecutively.

4. **Terminal 2.5D Parallax Fallback**:
   When an AI diffusion shot fails repeatedly due to model limitations, never drop back to a static image. Convert the approved keyframe into a multiplane 2.5D parallax sequence using depth slicing and continuous disparity warping.

---

## 2. Standard Workflow & Runbooks

Follow these progressive procedures when generating or auditing AI video:

### Phase 1: Scene & Motion Planning
Before rendering any pixels, compile the scene breakdown through the Motion Grammar.
- Read [MOTION_GRAMMAR.md](./runbooks/MOTION_GRAMMAR.md) for valid shot sizes, approved camera moves, and required acting beats.
- Run the prompt compiler:
  ```bash
  python skills/cinelogic-cinematics/scripts/format_prompt.py --subject "Napoleon on horseback" --beat "raising brass telescope" --secondary "smoke billowing across muddy field"
  ```

### Phase 2: Production & Generation
- Generate the style anchor / hero frame from pure text first.
- Condition the scene keyframes on the style anchor.
- For camera moves: apply the validated move vocabulary (track left/right, orbit left/right, dolly in/out, crane up/down).
- Read [PRODUCTION_PIPELINE.md](./runbooks/PRODUCTION_PIPELINE.md) for stage-by-stage instructions.

### Phase 3: Quality Control & Root-Cause Attribution
When reviewing candidate keyframes or clips:
- Run deterministic QC checks on keyframes:
  ```bash
  python skills/cinelogic-cinematics/scripts/qc_checker.py path/to/keyframe.png
  # Or check cut boundary continuity between adjacent shots:
  python skills/cinelogic-cinematics/scripts/qc_checker.py path/to/shotA_end.png --next-frame path/to/shotB_start.png
  ```
- If a clip fails, classify the root cause using [QC_AND_ROOT_CAUSE.md](./runbooks/QC_AND_ROOT_CAUSE.md):
  - `bad_keyframe`: Re-roll the keyframe anchor.
  - `weak_conditioning`: Increase anchor resolution or adjust framing.
  - `bad_prompt`: Strip conflicting action verbs.
  - `ltx_limitation`: Immediately divert to 2.5D Parallax Fallback.

### Phase 4: Film Pacing Audit
Inspect the complete video timeline to identify dead stretches and repetitive camera motions:
- Run the Pacing Inspector:
  ```bash
  python skills/cinelogic-cinematics/scripts/inspect_pacing.py path/to/rendered_video.mp4
  ```
- If dead runtime exceeds 20% or local motion drops below 4.0 on more than 2 consecutive shots, repair with 2.5D parallax or active motion re-renders.

### Phase 5: Parallax Fallback Deployment
- Read [FALLBACK_DOCTRINE.md](./runbooks/FALLBACK_DOCTRINE.md) for the exact 2.5D depth layering specifications.

---

## 3. Reference Runbooks

- [Production Pipeline](./runbooks/PRODUCTION_PIPELINE.md)
- [Motion Grammar & Camera Vocabulary](./runbooks/MOTION_GRAMMAR.md)
- [QC & Causal Root-Cause Diagnosis](./runbooks/QC_AND_ROOT_CAUSE.md)
- [2.5D Parallax Fallback Doctrine](./runbooks/FALLBACK_DOCTRINE.md)
