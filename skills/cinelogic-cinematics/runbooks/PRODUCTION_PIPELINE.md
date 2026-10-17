# End-to-End Production Pipeline Runbook

The complete multi-stage pipeline for producing an AI-directed film, from initial concept to master export.

---

## Stage-by-Stage Operational Map

```
Stage 01: Concept & Script Research
   |--> Factual extraction & compliance audit (PII / claims)
   |
Stage 02: Audio Synthesis & Forced Alignment
   |--> Sentence-level TTS synthesis (ElevenLabs / Chatterbox)
   |--> WhisperX word-level timing alignment (exact timestamps)
   |
Stage 03: Visual Direction & Motion Design
   |--> Shot duration clipping (<= 10.0 seconds per shot)
   |--> Motion grammar compiler (Shot size, Camera move, Beat, Physics)
   |
Stage 04: Style Anchor & Keyframing
   |--> Hero frame generated from text (no conditioning)
   |--> Scene keyframes conditioned on style anchor (Nano Banana / Flux)
   |
Stage 05: Video Generation & Camera Conditioning
   |--> Move-then-continue camera shots (81 frames @ 24 fps)
   |--> Remote / Local LTX generation with guidance=1.0
   |
Stage 06: Quality Control & Root-Cause Attribution
   |--> Deterministic filter (Luma, Sharpness, Letterbox, Boundary jump)
   |--> Vision Critic (Identity stability, style consistency)
   |--> Causal repair or 2.5D Parallax Fallback
   |
Stage 07: Timeline Pacing Audit & Assembly
   |--> Fourier phase-correlation pacing analysis (local_motion >= 4.0)
   |--> FFmpeg filtergraph transitions (CUT, DISSOLVE, WHIP_PAN, ZOOM_PUNCH)
   |--> Color grade & master render
```

---

## Production Rules & Guardrails

1. **Sentence Splitting**:
   - Never let a single generative video shot exceed 10.0 seconds. Video diffusion models experience temporal collapse and identity melting past ~120 frames (5 seconds at 24 fps).
   - If a voiceover sentence takes 16 seconds, split it at word boundaries into two 8-second shots with a natural cut.

2. **Style Anchor Discipline**:
   - The style anchor must be generated from **text only**. Never try to create an anchor by restyling an existing image—the model will simply echo the input.
   - All subsequent scene keyframes pass the hero style anchor as an image-to-image reference.

3. **Transition Continuity**:
   - When a cut is meant to continue an action, use the exact last frame of Shot A as the conditioning first frame of Shot B.
   - Check boundary difference: if the mean absolute luma diff exceeds 45.0, insert a cut transition rather than attempting a seamless blend.
