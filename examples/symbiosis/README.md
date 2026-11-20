# Symbiosis: The Multi-Agent Coding Orchestrator

**Symbiosis** is an advanced multi-agent orchestrator bundle that synthesizes the distinct superpowers of **Google Antigravity (`agy` / Gemini)** and **Anthropic Claude Code (`claude`)** into a rigorous, adversarial 6-stage software engineering pipeline.

---

## Architecture: The 6 Symbiotic Stages

```
1. Discovery & Constitution  --> claude:research (Haiku + xerj)  --> agy:architect (Gemini High + speckit-constitution)
2. Adversarial SDD           --> agy:architect (Gemini High)      --> claude:adversarial_reviewer (Opus) --> agy:architect (converge)
3. Planning & Isolation      --> claude:planner (Opus DAG)        --> omni (Git Worktree allocation & blast_radius guard)
4. Bifurcated Implementation --> claude:surgeon (Sonnet + xerj)   &   agy:builder (Gemini Medium + xerj-code)
5. Three-Tier Verification   --> claude:auditor (Opus)            --> agy:test_engineer (Gemini Medium)  --> claude:verifier (Sonnet)
6. Living Docs & Landing     --> agy:documenter (Gemini Low)      --> omni (Pre-commit gates, clean merge & persistence)
```

---

## Agent Roster & Assigned Subagents

| Subagent Name | Harness | Assigned Model | Tooling / Skills / MCP | Sacred Behavioral Rule |
| :--- | :--- | :--- | :--- | :--- |
| **`claude_research`** | `claude-sdk` | `claude-3-5-haiku` | `xerj` MCP stdio server | **Strict Read-Only**: Cites exact `file:line` evidence; never modifies code. |
| **`agy_architect`** | `antigravity` | `gemini-3.8-flash-high` | `speckit-constitution`, `speckit-specify`, `speckit-converge` | **Constitutional Authority**: Owns `constitution.md` and SDD spec; must resolve 100% of blocking issues. |
| **`claude_adversarial_reviewer`** | `claude-sdk` | `claude-3-opus` | Claude Native Reviewer | **Adversarial Critique**: Strict 3-tier triage (`BLOCKING`, `NON-BLOCKING`, `SUGGESTION`); formulate 3+ edge-case challenges. |
| **`claude_planner`** | `claude-sdk` | `claude-3-opus` | DAG Scheduler | **Non-Collision DAG**: Decomposes spec into atomic tasks; concurrent tasks never touch the same file. |
| **`claude_surgeon`** | `claude-sdk` | `claude-3-5-sonnet` | `xerj` MCP stdio server | **Precision Implementation**: Core algorithms, strict typing, runs local linter/test to Green. Co-signs commits. |
| **`agy_builder`** | `antigravity` | `gemini-3.8-flash-medium` | `xerj-code` reference | **High-Volume Scaffolding**: Fast generation of boilerplate, schemas, DTOs, migrations adhering to constitution. |
| **`claude_auditor`** | `claude-sdk` | `claude-3-opus` | Security / Concurrency Review | **Deep Security Audit**: Scrutinizes diffs for injection, memory leaks, race conditions, swallowed exceptions. |
| **`agy_test_engineer`** | `antigravity` | `gemini-3.8-flash-medium` | Spec-driven test suite | **Test Isolation**: Restricted exclusively to `tests/`; writes spec-driven tests and edge-case matrix. |
| **`claude_verifier`** | `claude-sdk` | `claude-3-5-sonnet` | Execution Gatekeeper | **Execution Gatekeeper**: Runs full test suites, checks real exit codes; renders binary `PASS` / `REJECT`. |
| **`agy_documenter`** | `antigravity` | `gemini-3.8-flash-low` | Documentation & OpenAPI | **Documentation Scope**: Strictly Markdown/OpenAPI only; provides manual human verification steps. |

---

## How to Run

### Option 1: Direct Session Launch via `omni run`
```bash
# Launch a session with Symbiosis in the background local server
omni run examples/symbiosis -p "Implement feature X following the 6-stage lifecycle"
```

### Option 2: Install as a Reusable Agent in Omnigent
```bash
# Register Symbiosis with your local Omnigent server
omni agent add examples/symbiosis

# Verify it appears in your installed agents
omni agent list

# Start a session by registered name
omni run --agent symbiosis -p "Analyze and implement issue #123"
```
