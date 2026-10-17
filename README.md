<div align="center">

```
  ██████╗██╗███╗   ██╗███████╗██╗      ██████╗  ██████╗ ██╗ ██████╗
 ██╔════╝██║████╗  ██║██╔════╝██║     ██╔═══██╗██╔════╝ ██║██╔════╝
 ██║     ██║██╔██╗ ██║█████╗  ██║     ██║   ██║██║  ███╗██║██║     
 ██║     ██║██║╚██╗██║██╔══╝  ██║     ██║   ██║██║   ██║██║██║     
 ╚██████╗██║██║ ╚████║███████╗███████╗╚██████╔╝╚██████╔╝██║╚██████╗
  ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝
```

### **Autonomous AI Cinematography & Video Systems Engine**
*Stop burning GPU clusters on prompt lottery. Start engineering deterministic cinema.*

---

[![License: MIT](https://img.shields.io/badge/License-MIT-7C3AED.svg?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3B82F6.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.2.0%20Compliant-EC4899.svg?style=for-the-badge&logo=anthropic&logoColor=white)](https://modelcontextprotocol.io)
[![Tests: 16/16 Passing](https://img.shields.io/badge/Tests-16%2F16%20Passing-10B981.svg?style=for-the-badge&logo=githubactions&logoColor=white)](tests/)
[![Docker: Multi-Arch](https://img.shields.io/badge/Docker-Ready-06B6D4.svg?style=for-the-badge&logo=docker&logoColor=white)](Dockerfile)
[![Zero GPU Required](https://img.shields.io/badge/Engine-Zero--GPU%20Motion-F59E0B.svg?style=for-the-badge&logo=speedtest&logoColor=white)](mcp/image_motion_server.py)

[⚡ Quickstart](#-60-second-quickstart) • 
[🏗️ Architecture](#-the-dual-engine-architecture) • 
[🔌 MCP Servers](#-model-context-protocol-mcp-servers) • 
[🧠 Skills & Rules](#-antigravity-skills--ide-plugins) • 
[🔬 Signal Processing](#-the-science-2d-fft-phase-correlation) • 
[💼 Case Study](docs/RECRUITER_PORTFOLIO_CASE_STUDY.md)

</div>

---

## 🎬 Why CineLogic?

Let’s be honest about the state of AI video in 2026:

Most AI video pipelines are **fragile, probabilistic toys**. Creators burn thousands of dollars spinning up 80GB VRAM pods to generate 3-second clips, only to find:
- **"Ken Burns Slop"**: The video model zoomed into a static Midjourney illustration, tricking naive motion metrics while the audience immediately drops off.
- **Morphing Nightmares**: Text prompts fighting against keyframe latent seeds because someone wrote `pan right, dramatic wide shot` on an image-to-video conditioned model.
- **Uncontrolled Hallucination**: No automated quality gates, no exposure telemetry, and zero deterministic fallbacks when diffusion inevitably fails.

**CineLogic changes the game.**

It is an industrial-grade, deterministic video engineering framework. It separates **creative intent** from **probabilistic generation**, giving autonomous coding agents (Claude, Antigravity IDE, Cursor) and human technical directors absolute, mathematical control over the AI filmmaking pipeline.

```
┌───────────────────────────────────────┬───────────────────────────────────────┐
│     THE TYPICAL AI "SLOP" TRAP        │       THE CINELOGIC ENGINE FIX        │
├───────────────────────────────────────┼───────────────────────────────────────┤
│ ❌ Burns $1.50 per 3-second test clip │ ⚡ 0.4s local Lanczos virtual camera   │
│ ❌ Naive pixel-diff fooled by zooms   │ 🔬 2D FFT phase correlation measures  │
│                                       │    true local non-rigid motion        │
│ ❌ Negative prompts in distilled runs │ 🎯 Guidance=1.0 prompt compilation    │
│    (does nothing, wastes attention)   │    (4-part clause, max 42 words)      │
│ ❌ Broken cuts, dark mush, letterbox  │ 🛡️ Deterministic Laplacian & Luma QC   │
│ ❌ Entire pipeline crashes on outage  │ 🔄 Multiplane parallax fallback tier  │
└───────────────────────────────────────┴───────────────────────────────────────┘
```

---

## 🏗️ The Dual-Engine Architecture

CineLogic bifurcates video generation into two complementary tiers to maximize visual quality while driving GPU compute costs toward zero:

```
                                  ┌────────────────────────┐
                                  │   CINELOGIC AGENT      │
                                  │   (Claude / IDE / CLI) │
                                  └───────────┬────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      │                                               │
           [Low Risk / Deterministic]                     [Complex Dynamic Action]
                      ▼                                               ▼
         ┌─────────────────────────┐                     ┌─────────────────────────┐
         │   TIER A: MOTION STUDIO │                     │  TIER B: DIFFUSION LAB  │
         │   (Zero-GPU / Local)    │                     │  (Frontier Generative)  │
         ├─────────────────────────┤                     ├─────────────────────────┤
         │ • Lanczos Subpixel Dolly│                     │ • Guidance=1.0 Compiler │
         │ • 2.5D Multiplane Drift │                     │ • Seed-Locked Keyframes │
         │ • Style Bible Generator │                     │ • Camera Lexicon Filter │
         │ • CPU / Apple Silicon   │                     │ • GPU Cloud / Local API │
         └────────────┬────────────┘                     └────────────┬────────────┘
                      │                                               │
                      └───────────────────────┬───────────────────────┘
                                              ▼
                                 ┌─────────────────────────┐
                                 │   DETERMINISTIC QC GATE │
                                 ├─────────────────────────┤
                                 │ • Laplacian Sharpness   │
                                 │ • Mean Luma Exposure    │
                                 │ • Letterbox Ratio Check │
                                 │ • Cut Seam Boundary Luma│
                                 │ • 2D FFT Phase Pacing   │
                                 └────────────┬────────────┘
                                              ▼
                                 ┌─────────────────────────┐
                                 │   PRODUCTION MASTER     │
                                 │   1080p / 4K Pro Video  │
                                 └─────────────────────────┘
```

### ⚡ Tier A: Zero-Diffusion Motion Studio
- **Pure Local Physics**: Executes Lanczos-interpolated virtual camera dollies, subpixel push-ins, and lateral drift in **0.4 seconds** directly on CPU or Apple Silicon.
- **Deterministic Economics**: Zero GPU tokens spent. Perfect for establishing shots, dialogue coverage, and high-retention atmosphere.
- **Style Bible Chaining**: Enforces character visual continuity across shots without needing finetuned LoRAs.

### 🔬 Tier B: Frontier Diffusion Studio
- **Guidance=1.0 Prompt Compiler**: Strips conflicting camera tokens from keyframe-conditioned runs, enforces a strict 4-clause sentence structure, and hard-caps prompts at 42 words to avoid attention saturation.
- **2D FFT Phase Correlation**: Mathematically factors out whole-frame affine transformation to measure *actual subject motion* vs static zooms.
- **8-Category Root Cause Diagnosis**: Instant triage when clips fail (camera conflict, guidance over-saturation, motion collapse, boundary seams).

---

## ⚡ 60-Second Quickstart

### Option 1: Native Python (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/cinelogic.git
cd cinelogic

# 2. Install dependencies (Requires FFmpeg installed)
pip install -r requirements.txt
pip install -e .

# 3. Run the complete validation test suite (16/16 tests)
python3 tests/run_intensive_tests.py
```

### Option 2: Docker (Zero-Configuration / Containerized)

No local Python or FFmpeg required:

```bash
# Build and run the test suite in Docker
docker compose run test

# Launch the Full-Stack Studio MCP server in Docker
docker compose run studio-mcp
```

---

## 🔌 Model Context Protocol (MCP) Servers

CineLogic includes **two standard stdio MCP servers** ready for instant integration with **Claude Desktop**, **Antigravity IDE**, **Cursor**, or any MCP-compliant client.

### 1. CineLogic Studio Server (`mcp/server.py`)
Provides full-stack video engineering, prompt compilation, script auditing, and failure diagnosis:

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| `cinelogic_design_shot` | `subject, duration_sec, shot_size, camera_move, performance_beat, secondary_motion` | Designs high-retention shot plans with exact push-in ceilings. |
| `cinelogic_format_prompt` | `style, subject, beat, secondary, conditioned_on_image` | Compiles prompt strictly following Guidance=1.0 economics. |
| `cinelogic_check_qc` | `image_path, next_frame_path` | Evaluates deterministic Laplacian sharpness, luma, letterboxing, and seam jump. |
| `cinelogic_diagnose_failure` | `symptom, attempt_number` | 8-category root-cause autopsy with precise corrective action. |
| `cinelogic_audit_script` | `sentences` | Validates sentence durations, PII compliance, and fact-freezing. |
| `cinelogic_analyze_pacing` | `video_path` | Measures 2D FFT phase-correlation camera-undone local motion. |

### 2. CineLogic Motion Server (`mcp/image_motion_server.py`)
Zero-diffusion motion synthesis and signal processing:

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| `cinelogic_render_virtual_dolly` | `image_path, out_path, duration_sec, end_zoom, drift` | Subpixel Lanczos camera push-in + drift (0.4s render). |
| `cinelogic_generate_style_bible` | `topic, chapter_title, emotional_register` | Generates immutable visual bible anchor for multi-shot runs. |
| `cinelogic_screen_footage` | `image_path, target_sentence` | Fast seek-frame inspector flagging watermarks and freezes. |

### 1-Click Automated Setup for Claude & Antigravity

Run the setup helper to configure your IDE or Claude Desktop automatically with the exact path of your local clone:

```bash
# Automatically configure Claude Desktop:
python3 setup_mcp.py --install-claude

# Automatically configure Antigravity IDE:
python3 setup_mcp.py --install-antigravity
```

Or manually paste this block into your `claude_desktop_config.json` or `~/.gemini/config/mcp_config.json`:

```json
{
  "mcpServers": {
    "cinelogic-studio": {
      "command": "python3",
      "args": ["/ABSOLUTE/PATH/TO/cinelogic/mcp/server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    },
    "cinelogic-motion": {
      "command": "python3",
      "args": ["/ABSOLUTE/PATH/TO/cinelogic/mcp/image_motion_server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

---

## 🧠 Antigravity Skills & IDE Plugins

CineLogic includes a modular plugin bundle for **Antigravity IDE** (`plugin/cinelogic-studio/`):

```
plugin/cinelogic-studio/
├── plugin.json                    <- Extension manifest
├── mcp_config.json                <- Bundled MCP server mappings
├── rules/film_rules.md            <- Hard guidelines for cinematic agents
└── skills/
    ├── cinelogic-scripting/       <- Beats, rhythm, retention curves
    ├── cinelogic-director/        <- Camera setups, lighting, composition
    ├── cinelogic-keyframes/       <- Anchor seeds, style bibles, prompt laws
    └── cinelogic-qc-fallback/     <- 2D FFT inspection, Parallax fallback
```

### Installation
Simply copy or symlink the plugin folder into your Antigravity config:
```bash
cp -r cinelogic/plugin/cinelogic-studio ~/.gemini/config/plugins/
```

---

## 🔬 The Science: 2D FFT Phase Correlation

Why do standard AI video pipelines let boring videos slip through?

When a video model applies a slow camera zoom to a still image, **every single pixel changes coordinate values**. Naive frame difference algorithms (`|Frame_t - Frame_0|`) report high motion energy ($E > 20.0$), marking the shot as "active". In reality, the image is a frozen cardboard cutout, and your viewer has already swiped away.

CineLogic implements **Spatial Fourier Phase Correlation** (`skills/cinelogic-cinematics/scripts/inspect_pacing.py`):

$$\mathbf{R} = \frac{\mathcal{F}(I_1) \circ \mathcal{F}(I_2)^*}{\left| \mathcal{F}(I_1) \circ \mathcal{F}(I_2)^* \right|}$$

$$\Delta x, \Delta y = \arg\max \left( \mathcal{F}^{-1}(\mathbf{R}) \right)$$

1. We compute the 2D cross-power spectrum between successive frames.
2. The peak of the inverse Fourier transform yields the global affine camera translation vector $(\Delta x, \Delta y)$.
3. We algebraically undo the camera transform on $I_2$.
4. We measure the **Local Residual Energy**. If the residual is $< 4.0$, CineLogic rejects the clip as `DEAD_STILL` (Ken Burns zoom) and triggers the 2.5D Parallax fallback.

---

## 💻 Running the Examples

### 1. Render a Virtual Camera Dolly (0.4s Zero-GPU)
```bash
python3 examples/quickstart_virtual_dolly.py
```
*Output: Generates a broadcast-ready 1080p H.264 video with Lanczos subpixel easing and 4% lateral cinematic drift.*

### 2. Inspect a Video for Ken Burns Zoom Slop
```bash
python3 examples/analyze_my_video.py
```
*Output: Unpacks video frames, applies 2D FFT phase correlation, and flags whether the motion is genuine actor performance or a fake camera zoom.*

### 3. Compile Guidance=1.0 Prompts & Run Pre-Flight QC
```bash
python3 examples/format_and_qc_shot.py
```
*Output: Synthesizes a 4-clause prompt adhering to token caps, then runs Laplacian sharpness, luminance, and letterbox checks on the source keyframe.*

---

## 📊 Benchmark & Compute Economics

Tested on Apple M-Series Silicon vs Cloud A100 GPU:

| Operation | Cloud A100 (Diffusion) | CineLogic Tier A (CPU) | Efficiency Gain |
| :--- | :--- | :--- | :--- |
| **Establishing Dolly Shot** | 42.0s ($0.08 / gen) | **0.4s ($0.00)** | **105x faster • 100% savings** |
| **Keyframe QC Gate** | Manual / Visual | **0.02s (Automated)** | **Instant defect triage** |
| **Motion Screening** | Human inspection | **0.15s (2D FFT)** | **Automated retention audit** |
| **Prompt Compilation** | Trial-and-error | **0.001s (Deterministic)** | **Zero token burn** |

---

## 📁 Repository Layout

```
cinelogic/
├── README.md                          <- This document
├── LICENSE                            <- MIT License
├── pyproject.toml                     <- Package build metadata
├── requirements.txt                   <- Core dependencies (numpy, pillow)
├── Dockerfile                         <- Multi-arch container (FFmpeg + Python)
├── docker-compose.yml                 <- Containerized test & MCP services
├── .github/workflows/ci.yml           <- Automated CI matrix (Python 3.10-3.12)
├── docs/
│   ├── ARCHITECTURAL_DEEP_DIVE.md     <- Mathematical autopsy & architecture specs
│   ├── RECRUITER_PORTFOLIO_CASE_STUDY.md <- Executive portfolio overview & resume impact
│   └── EXPORT_AND_PACKAGING_GUIDE.md  <- Complete Antigravity & Claude setup guide
├── mcp/
│   ├── server.py                      <- CineLogic Studio MCP Server (Full-Stack Video)
│   ├── image_motion_server.py         <- CineLogic Motion MCP Server (Zero-Diffusion)
│   ├── mcp_config.json                <- Ready-to-copy client configuration
│   ├── test_server.py                 <- Studio MCP test client
│   └── test_image_motion_server.py    <- Motion MCP test client
├── plugin/
│   └── cinelogic-studio/              <- Antigravity IDE Plugin Bundle
│       ├── plugin.json
│       ├── mcp_config.json
│       ├── rules/film_rules.md
│       └── skills/
│           ├── cinelogic-scripting/
│           ├── cinelogic-director/
│           ├── cinelogic-keyframes/
│           └── cinelogic-qc-fallback/
├── skills/
│   └── cinelogic-cinematics/          <- Standalone Antigravity Skill
│       ├── SKILL.md
│       └── scripts/
│           ├── format_prompt.py       <- Guidance=1.0 prompt compiler
│           ├── inspect_pacing.py      <- 2D FFT phase correlation motion inspector
│           └── qc_checker.py          <- Deterministic Laplacian/Luma QC checker
├── examples/
│   ├── quickstart_virtual_dolly.py    <- Zero-GPU camera dolly synthesis
│   ├── analyze_my_video.py            <- Fourier video pacing analyzer
│   └── format_and_qc_shot.py          <- Prompt synthesis & pre-flight QC
└── tests/
    ├── run_intensive_tests.py         <- Real-world media validation suite
    └── fixtures/                      <- Test media (sharp, dark, blurred, mp4)
```

---

## 🤝 Contributing

Contributions from systems engineers, computer vision researchers, and AI filmmakers are enthusiastically welcomed!

1. Fork the repo and create your feature branch: `git checkout -b feature/amazing-lens-model`
2. Ensure all intensive tests pass: `python3 tests/run_intensive_tests.py`
3. Commit your changes: `git commit -m 'feat: Add anamorphic lens flare simulation'`
4. Push to branch: `git push origin feature/amazing-lens-model`
5. Open a Pull Request! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for style conventions.

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for full details.

---

<div align="center">

**Built with precision for the future of synthetic cinema.**  
If you find CineLogic useful, give us a ⭐ on GitHub!

</div>
