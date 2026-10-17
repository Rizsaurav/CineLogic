---
name: cinelogic-scripting
description: >-
  Audits, structures, and writes narrative video scripts optimized for AI visual production.
  Use this skill when drafting documentary or story scripts, verifying claims, enforcing
  PII/compliance rules, budgeting sentence durations for diffusion horizons, or checking
  repetition.
---

# CineLogic Scripting: Narrative Architecture & Compliance

This skill enforces the storytelling and compliance doctrines developed in CineLogic, ensuring scripts are not just engaging, but mathematically viable for video diffusion pipelines.

---

## 1. Core Principles

1. **The 10-Second Diffusion Horizon**:
   - Spoken sentences must fit into shots of **10.0 seconds or less** (typically 20-25 words at standard speaking rate).
   - If a complex historical idea takes 18 seconds, split it into two sentences at a logical breath or clause boundary.

2. **Compliance & Fact-Freezing**:
   - **No PII**: Never include names of non-public private individuals.
   - **Financial Policy**: Financial figures (exact revenues, valuations, settlements) require explicit verification to avoid hallucinated economic claims.
   - **Fact Sheet Freezing**: Freeze core historical dates, troop numbers, locations, and geography into a verified factsheet before writing narration.

3. **Retention & Hook Mechanics**:
   - **The 3-Second Opening Hook**: The opening sentence must establish high stakes ("In October 1813, half a million men converged on a single city...").
   - **No Passive Exposition**: Ground narration in visible physical reality (armies marching, ink drying on treaties, rain on cobblestones) rather than abstract philosophical ruminations.

---

## 2. Standard Workflow

1. **Fact Gathering & Verification**: Compile facts into `factsheet.json`.
2. **Draft Narration**: Write sentence-by-sentence with clear emotional beats.
3. **Budget Word Counts**:
   ```
   Words <= 25 -> Single 10s shot
   Words > 25  -> Mark for sentence split into Shot A and Shot B
   ```
4. **Compliance Pass**: Use MCP tool `cinelogic_audit_script` or inspect for names and figures.

