# CineLogic Packaging & Deployment Guide
*How to export, distribute, and install CineLogic as an Antigravity Plugin, MCP Servers, or standalone Python tooling.*

---

## 1. Distribution Options

CineLogic is architected to be modular and deployable in three distinct tiers:

```
+-------------------------------------------------------------------------+
|                    TIER 1: ANTIGRAVITY PLUGIN & SKILLS                  |
|   Drop plugin/cinelogic-studio/ into ~/.gemini/config/plugins/          |
|   Teaches any AI agent the visual runbooks, prompt rules, and heuristics|
+-------------------------------------------------------------------------+
                                    +
+-------------------------------------------------------------------------+
|                           TIER 2: DUAL MCP SERVERS                      |
|   Connects to Antigravity IDE or Claude Desktop via Model Context       |
|   Protocol (stdio JSON-RPC). Gives LLMs direct access to QC, prompt,    |
|   and virtual camera tools.                                             |
+-------------------------------------------------------------------------+
                                    +
+-------------------------------------------------------------------------+
|                       TIER 3: STANDALONE SCRIPTS                        |
|   Terminal CLI tools for local pacing FFT analysis, deterministic QC    |
|   gating, and batch prompt compilation.                                 |
+-------------------------------------------------------------------------+
```

---

## 2. Installing as an Antigravity Plugin / Skill

To make CineLogic natively available to Antigravity IDE across all workspaces:

### Option A: Install Complete Plugin (Recommended)
Copy the `cinelogic-studio` plugin bundle to your global Antigravity configuration directory:
```bash
cp -r cinelogic/plugin/cinelogic-studio ~/.gemini/config/plugins/
```
This automatically registers:
- The 4 modular skills (`cinelogic-scripting`, `cinelogic-director`, `cinelogic-keyframes`, `cinelogic-qc-fallback`)
- The workspace cinematography rules
- Both MCP servers (`cinelogic-studio` and `cinelogic-motion`)

### Option B: Standalone Skill
Copy just the cinematics skill:
```bash
cp -r cinelogic/skills/cinelogic-cinematics ~/.gemini/config/skills/
```

---

## 3. Registering the Model Context Protocol (MCP) Servers

CineLogic includes two MCP servers running over standard I/O (stdio) using only the Python standard library.

### Automated 1-Click Setup (Recommended)
Run the automated configuration script from the `cinelogic` repository:

```bash
# For Antigravity IDE:
python3 setup_mcp.py --install-antigravity

# For Claude Desktop:
python3 setup_mcp.py --install-claude
```

### Manual Configuration

#### In Antigravity IDE
Add the servers to `~/.gemini/config/mcp_config.json`:
```json
{
  "mcpServers": {
    "cinelogic-studio": {
      "command": "python3",
      "args": [
        "<PATH_TO_CINELOGIC>/mcp/server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    },
    "cinelogic-motion": {
      "command": "python3",
      "args": [
        "<PATH_TO_CINELOGIC>/mcp/image_motion_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

#### In Claude Desktop
Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "cinelogic-studio": {
      "command": "python3",
      "args": [
        "<PATH_TO_CINELOGIC>/mcp/server.py"
      ]
    },
    "cinelogic-motion": {
      "command": "python3",
      "args": [
        "<PATH_TO_CINELOGIC>/mcp/image_motion_server.py"
      ]
    }
  }
}
```

Now, Claude or Antigravity can directly invoke:
- `cinelogic_design_shot`
- `cinelogic_format_prompt`
- `cinelogic_check_qc`
- `cinelogic_diagnose_failure`
- `cinelogic_audit_script`
- `cinelogic_analyze_pacing`
- `cinelogic_render_virtual_dolly`
- `cinelogic_generate_style_bible`
- `cinelogic_screen_footage`

---

## 4. Standalone CLI Usage for Creators

If you just want to run the scripts from your terminal during production:

### Pacing Analysis (Detect Ken Burns Still Zoom Traps):
```bash
python3 cinelogic/skills/cinelogic-cinematics/scripts/inspect_pacing.py /path/to/shot.mp4
```

### Frame & Continuity Seam QC:
```bash
python3 cinelogic/skills/cinelogic-cinematics/scripts/qc_checker.py shot_frame.png --next-frame next_frame.png
```

### Optimal Guidance Prompt Compiler:
```bash
python3 cinelogic/skills/cinelogic-cinematics/scripts/format_prompt.py \
  --subject "Samurai drawing katana" \
  --beat "stepping forward into low stance" \
  --secondary "cherry blossom petals swirling in dust"
```
