# CineLogic Film Production Directives

When writing code, scripts, or video prompts in this workspace:

1. **Diffusion Horizon**: Keep all generative video shots under 10.0 seconds (<= 25 spoken words per sentence).
2. **Push-In Constraint**: Ensure push-in shots (`dolly_in`) do not exceed 25% of the total shots planned for any film.
3. **Guidance Scale 1.0 Economics**: Strip camera motion terms and style adjectives from keyframe-conditioned text prompts; style belongs exclusively to the conditioning keyframe anchor.
4. **Pacing Gate**: Any candidate video clip with camera-undone local motion below 4.0 must be flagged as a Ken Burns static zoom and diverted to 2.5D Parallax fallback.
