# Omnigent

<div align="center">

### Terminal-First Multi-Agent CLI Orchestrator

**Orchestrating Google Antigravity (`agy` / Gemini) and Anthropic Claude Code (`claude`) natively across the 6 Sacred Stages of software engineering.**

[![GitHub Repo](https://img.shields.io/badge/GitHub-Death0512%2FOmnigent-blue?logo=github)](https://github.com/Death0512/Omnigent)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/Death0512/Omnigent/blob/main/LICENSE)
[![Python: 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Status: Active](https://img.shields.io/badge/status-active-brightgreen.svg)]()

</div>

---

## Overview

**Omnigent** (`omni`) is a high-performance, terminal-first multi-agent orchestration runtime built for Linux and WSL2.

Rather than running heavy web dashboards or creating third-party proxy wrappers, Omnigent operates natively in your terminal. It acts as a conductor over your authentic, locally installed developer CLI harnesses:
* **Google Antigravity (`agy`)** powered by **Gemini 3.8 Flash** models (`~/.gemini/`).
* **Anthropic Claude Code (`claude`)** powered by **Claude 3.5 Sonnet, Haiku, & Opus** (`~/.claude/`).

By leveraging the native TUI, tmux process isolation, and asynchronous event-driven dispatch, Omnigent coordinates specialized agents to work together systematically through a structured 6-stage software development lifecycle called **Symbiosis**.

---

## Key Highlights

- **Terminal-First & Zero Bloat**: No Node.js / pnpm runtime dependencies, no Web UI server overhead, and no Electron windows. Pure Python 3.12+ CLI (`omni` / `omnigent`).
- **Authentic Dual-Harness Execution**: Directly bridges your genuine local CLI sessions (`agy` and `claude`) using authentic local credentials.
- **Strict Model Hard-Pinning**: Explicitly constrains model tiers based on computational and reasoning demands, preventing expensive unpinned token waste.
- **Adversarial & Spec-Driven**: Combines Google Antigravity's rapid scaffolding and constitutional specifications with Anthropic Claude's deep reasoning, adversarial review, and architectural auditing.
- **Reactive Wakeups & Asynchronous Subagents**: Subagents execute concurrently in isolated terminal sessions. Outcomes land asynchronously in the orchestrator's inbox (`sys_read_inbox`) without costly polling loops.
- **Full ToS & Boundary Compliance**: Complies strictly with vendor terms of service. The orchestrator transparently identifies as Antigravity High leading the workflow rather than claiming to be a proprietary wrapped third-party entity.

---

## Architecture: The Symbiosis Workflow

The flagship orchestrator bundle in Omnigent is **Symbiosis**. It synthesizes the distinct superpowers of Google Antigravity and Anthropic Claude Code into a 6-stage pipeline:

```
1. Discovery & Constitution  --> claude:research (Haiku)       --> agy:architect (Flash High)
2. Adversarial SDD           --> agy:architect (Draft Spec)   --> claude:adversarial_reviewer (Opus Red-Team) --> agy:architect (Converge)
3. Planning & Allocation     --> claude:planner (Opus DAG)     --> omni (Task Isolation & Blast Radius Guard)
4. Bifurcated Implementation --> claude:surgeon (Sonnet Logic) &   agy:builder (Flash Medium Scaffolding)
5. Three-Tier Verification   --> claude:auditor (Opus Audit)  --> agy:test_engineer (Spec Tests) --> claude:verifier (Sonnet Gatekeeper)
6. Living Docs & Landing     --> agy:documenter (Flash Low)   --> omni (Pre-commit gates & clean git merge)
```

### The 6 Sacred Stages

1. **Discovery & Constitution**:
   - `claude_research` performs strict read-only reconnaissance, citing exact `file:line` locations into `recon_report.md`.
   - `agy_architect` seals project invariants and non-negotiable boundaries into `constitution.md`.
2. **Adversarial SDD (Software Design Document)**:
   - `agy_architect` drafts the specification in `spec.draft.md`.
   - `claude_adversarial_reviewer` executes an adversarial red-team critique with 3-tier triage (`BLOCKING`, `NON-BLOCKING`, `SUGGESTION`) into `spec_review.md`.
   - `agy_architect` resolves 100% of blocking issues to freeze `spec.final.md`.
3. **Planning & Allocation**:
   - `claude_planner` decomposes the frozen spec into atomic, non-colliding DAG tasks saved to `tasks_dag.yaml`.
4. **Bifurcated Implementation**:
   - `claude_surgeon`: Precision surgery for complex core algorithms, state machines, and concurrency logic.
   - `agy_builder`: High-volume scaffolding, database schemas, migrations, DTOs, and boilerplate code.
5. **Three-Tier Adversarial Verification**:
   - `claude_auditor`: Security audit, memory leak checks, race condition analysis, and invariant verification on diffs (`audit_report.md`).
   - `agy_test_engineer`: Spec-driven test authoring isolated within `tests/`.
   - `claude_verifier`: Executes the test suite, verifies real process exit codes, and renders a binary **PASS** or **REJECT**.
6. **Living Documentation & Merge**:
   - `agy_documenter`: Updates documentation, changelogs, and concrete human verification steps.
   - Git merge gates and pre-commit checks ensure clean landing.

---

## Sub-Agent Roster

Symbiosis declares exactly 10 specialized subagents:

| Sub-Agent | Platform & Harness | Model Tier | Core Responsibility |
| :--- | :--- | :--- | :--- |
| **`claude_research`** | Claude-native | `claude-3-5-haiku` | Strict read-only reconnaissance; cites exact `file:line` evidence. |
| **`agy_architect`** | Antigravity-native | `gemini-3.8-flash-high` | Constitutional authority; authors SDD and seals project boundaries. |
| **`claude_adversarial_reviewer`** | Claude-native | `claude-3-opus` | Adversarial red-team review; triages edge cases and potential failure modes. |
| **`claude_planner`** | Claude-native | `claude-3-opus` | Non-collision DAG task decomposition. |
| **`claude_surgeon`** | Claude-native | `claude-3-5-sonnet` | Core algorithms, complex typing, async concurrency implementation. |
| **`agy_builder`** | Antigravity-native | `gemini-3.8-flash-medium` | Scaffolding, migrations, DTOs, schemas, boilerplate generation. |
| **`claude_auditor`** | Claude-native | `claude-3-opus` | Deep security audit, async safety, and git diff inspection. |
| **`agy_test_engineer`** | Antigravity-native | `gemini-3.8-flash-medium` | Spec-driven unit and integration test suite authoring in `tests/`. |
| **`claude_verifier`** | Claude-native | `claude-3-5-sonnet` | Test execution gatekeeper; validates process exit codes (PASS / REJECT). |
| **`agy_documenter`** | Antigravity-native | `gemini-3.8-flash-low` | Living documentation, OpenAPI specs, and human testing instructions. |

---

## Installation & Setup

### Prerequisites

- **OS**: Linux or WSL2 on Windows.
- **Python**: Version `3.12` or newer.
- **Package Manager**: [`uv`](https://docs.astral.sh/uv/) (recommended).
- **Terminal Utilities**: `tmux`, `git`, `bash`.
- **Harness CLIs**:
  - Google Antigravity CLI (`agy`) installed and authenticated (`~/.gemini/`).
  - Anthropic Claude Code CLI (`claude`) installed and authenticated (`~/.claude/` or `ANTHROPIC_API_KEY`).

### Install from Source

```bash
# 1. Clone the repository
git clone https://github.com/Death0512/Omnigent.git
cd Omnigent

# 2. Install editable CLI using uv
uv tool install --force --editable .

# 3. Verify installation
omni --help
```

---

## Quickstart & Usage

### 1. Run the Symbiosis Orchestrator

Launch a symbiotic multi-agent session directly from your terminal:

```bash
omni symbiosis -p "Analyze the authentication module and implement OAuth refresh rotation"
```

For a one-off headless execution:
```bash
omni symbiosis --no-session -p "Investigate issue #42 and provide the complete fix"
```

### 2. Standalone Harness Launchers

You can also launch individual native CLI harnesses directly through Omnigent:

```bash
# Launch Google Antigravity CLI session
omni antigravity

# Launch Anthropic Claude Code CLI session
omni claude
```

### 3. Session & Process Management

```bash
# Check status of running sessions and background daemons
omni doctor

# Stop background runners and clean up active sessions
omni stop
```

---

## Development & Verification

Omnigent maintains strict quality and formatting standards via `uv`, `ruff`, and `pytest`:

```bash
# Run unit and integration tests
uv run --no-sync pytest tests/

# Run fast code linting and style checks
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
```

---

## Author & License

- **Author**: [Death0512](https://github.com/Death0512) (`damanhqaz01@gmail.com`)
- **License**: [Apache License 2.0](LICENSE)
