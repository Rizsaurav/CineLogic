# Contributing to CineLogic

First off, thank you for considering contributing to CineLogic! Whether you're adding a new camera trajectory, refining Fourier phase correlation parameters, or improving MCP tool schemas, your help makes deterministic AI filmmaking better for everyone.

---

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rizsaurav/CineLogic.git
   cd cinelogic
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Prerequisites**:
   - `ffmpeg` and `ffprobe` must be accessible in your system PATH (`brew install ffmpeg` on macOS, `sudo apt install ffmpeg` on Ubuntu).

---

## Running the Test Suite

Before submitting any Pull Request, ensure that the intensive test suite passes with a 100% success rate:

```bash
python3 tests/run_intensive_tests.py
python3 mcp/test_server.py
python3 mcp/test_image_motion_server.py
```

---

## Contribution Guidelines

1. **Combinatorial Directing Rules**:
   - CineLogic adheres strictly to the **25% Push-In Ceiling** and the **Rule of Three** (no move family or shot size repeated 3 times consecutively). Any new director heuristics must maintain these combinatorial constraints.
2. **Guidance=1.0 Economics**:
   - Diffusion prompts must not contain camera motion keywords when keyframe conditioning is present. Style belongs exclusively to the conditioning keyframe anchor.
3. **Pacing Invariants**:
   - All motion metrics must decouple camera movement from character movement. Any changes to `inspect_pacing.py` must maintain the `MIN_LOCAL_MOTION = 4.0` threshold.
4. **Code Style**:
   - Python 3.9+ typing annotations.
   - Zero external transport dependencies for MCP servers (pure Python stdlib JSON-RPC over `stdio`).

---

## Pull Request Process

1. Fork the repo and create your branch from `main`:
   ```bash
   git checkout -b feat/my-new-camera-move
   ```
2. Commit your changes with descriptive commit messages.
3. Push to your fork and submit a Pull Request.
4. CI will run the test matrix across Python 3.10, 3.11, and 3.12.
