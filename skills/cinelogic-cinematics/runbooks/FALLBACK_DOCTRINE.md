# 2.5D Parallax Fallback Doctrine

When video diffusion models fail complex motion or character consistency, the professional filmmaker does not accept deformed output or static slide shows. The CineLogic fallback pipeline converts approved 2D keyframes into cinematic multiplane parallax shots.

---

## The Technical Execution Pipeline

```
+---------------------------------------------------------------+
|                       APPROVED 2D KEYFRAME                     |
+---------------------------------------------------------------+
                               |
                               v
+---------------------------------------------------------------+
|                    DEPTH ESTIMATION (MPS/CUDA)                |
|      Depth Anything V2 Small -> Relative Disparity [0, 1]     |
+---------------------------------------------------------------+
                               |
                               v
+---------------------------------------------------------------+
|                 COLOR-GUIDED EDGE REFINEMENT                  |
|    Bilateral color guided filter snaps continuous depth       |
|    onto dark cel ink outlines to prevent halos                |
+---------------------------------------------------------------+
                               |
                               v
+---------------------------------------------------------------+
|                   1D K-MEANS LAYER QUANTIZATION               |
|      Disparity is partitioned into 3 to 5 discrete planes     |
|      (Foreground, Subject, Midground, Background, Sky)        |
+---------------------------------------------------------------+
                               |
                               v
+---------------------------------------------------------------+
|                 PUSH-PULL PYRAMID INPAINTING                  |
|   Reveals occluded background behind near objects without     |
|   slow generative inpainting                                  |
+---------------------------------------------------------------+
                               |
                               v
+---------------------------------------------------------------+
|                CONTINUOUS DISPARITY WARPING                   |
|   Each plane slides with differential velocity                |
|   Augmented with +/-3% exposure breath & floating dust motes  |
+---------------------------------------------------------------+
                               |
                               v
+---------------------------------------------------------------+
|            HIGH-RETENTION CINEMATIC FALLBACK CLIP             |
|   Local motion = 4.2 - 8.2 (Clears pacing threshold 4.0)      |
+---------------------------------------------------------------+
```

---

## Parallax Implementation Parameters

1. **Disparity Floor (`D_FLOOR = 0.08`)**:
   Never let the background plane remain 100% frozen. In real photography, only true astronomical infinity has zero parallax. A slight drift on the background wall prevents the shot from looking like a theatrical cardboard cutout.

2. **Base Oversample (`BASE_OVERSAMPLE = 1.1`)**:
   Scale the source image to 110% before warping. This ensures camera push-ins do not cause bilinear interpolation blur or shimmering cel lines.

3. **Atmospheric Breathing**:
   Modulate global exposure subtly across the shot duration ($\pm 3\%$ luminance variation) and add 12–24 subtle drifting light motes. The human eye interprets these subtle physical cues as live camera presence.
