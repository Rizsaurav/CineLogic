# Cinematic Motion Grammar & Constraint Reference

This document codifies the combinatorial rules that prevent visual fatigue and enforce cinematic rhythm in AI-generated films.

---

## 1. Shot Sizes and Framing Order

Use five standardized shot sizes:

| Shot Size | Identifier | Framing Guidelines |
|---|---|---|
| Extreme Wide | `extreme_wide` | Landscape / environment dominates; human figures < 10% screen height |
| Wide | `wide` | Full human body visible with ample headroom and surrounding context |
| Medium | `medium` | Waist-up framing; ideal for character interactions and hand gestures |
| Close-Up | `close` | Shoulders and head; emphasizes facial emotion and dialogue |
| Extreme Close-Up | `extreme_close` | Focused on eyes, hands, weapons, or small key story objects |

### Hard Constraint: Shot Size Repetition
- **NEVER** use the same shot size 3 times consecutively.
- Transitioning between extreme ends (e.g., Extreme Wide directly to Extreme Close-Up) should be reserved for dramatic shock beats. Standard narrative flow steps by 1 or 2 framing levels.

---

## 2. Approved Camera Moves Vocabulary

Only use camera moves that diffusion models (such as LTX-2.5, Kling, Runway) execute reliably from a conditioning frame:

| Camera Move | Identifier | Description & LTX Reliability |
|---|---|---|
| Track Left | `track_left` | Lateral slide left; maintains orientation while parallaxing foreground |
| Track Right | `track_right` | Lateral slide right; reveals background behind subjects |
| Dolly In | `dolly_in` | Physical push toward subject; intensifies focus (max 25% of all shots) |
| Dolly Out | `dolly_out` | Physical pull back; reveals scope and isolation |
| Crane Up | `crane_up` | Vertical elevation; great for transitioning from subject to horizon |
| Crane Down | `crane_down` | Vertical descent; establishes intimacy from an environment |
| Arc Left | `arc_left` | Short 20-30 degree circular curve around subject |
| Arc Right | `arc_right` | Short circular curve; gives three-dimensional depth |
| Handheld Follow | `handheld_follow` | Organic slight drift; conveys documentary urgency |
| Focus Pull | `focus_pull` | Foreground subject holds while background depth shifts |
| Tilt Up | `tilt_up` | Vertical pitch from feet/ground to eyes/sky |

### Forbidden Camera Motions (The "Do Not Use" List)
1. **In-Shot Whip Pans / Cuts**: Prompts containing "whip pan to another room" or "cut to" cause the model to violently morph geometry mid-shot. Whips belong to the edit timeline (`EditTransition.WHIP_PAN`), never the generative diffusion prompt.
2. **Full 360 Orbits**: The model cannot hallucinate the unconditioned back of a set without severe identity drift.
3. **Locked-Off / Static**: Avoid prompting "the camera stays completely still" unless intentionally creating a high-contrast still frame; diffusion models interpret static camera prompts by freezing all internal character movement.

---

## 3. The 4-Part Prompt Formula (Guidance Scale = 1.0)

For diffusion models conditioned on a keyframe, construct prompts using this strict 4-part clause:

$$\text{Final Prompt} = [\text{Style}] + [\text{Subject}] + [\text{Performance Beat}] + [\text{Secondary Motion}]$$

### Example Breakdown:
- **Style**: `Vivid historical anime, dark ink linework, saturated cel shading.`
- **Subject**: `Napoleon Bonaparte standing on the wooden observation platform.`
- **Performance Beat**: `His right hand swiftly unfurls a wrinkled parchment map.`
- **Secondary Motion**: `Wool coat tails flapping violently in the cold autumn wind as lantern soot drifts.`

**Notice what is missing**: No camera move words in the prompt when conditioned on an image! The camera vector is either handled by spatial guide latents (C1/C2) or camera motion LoRAs.
