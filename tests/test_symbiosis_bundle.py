"""Tests for Symbiosis bundle loading, datamodel translation, prompt composition,
and tool wiring.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from omnigent.inner.datamodel import AgentDef, ExecutorSpec
from omnigent.inner.executor import MockExecutor, ToolCallRequest, TurnComplete
from omnigent.inner.loader import load_agent_def_from_path
from omnigent.inner.tools import AgentTool
from omnigent.runtime.prompt import (
    SUBAGENT_WAKE_NOTICE_INSTRUCTION,
    WORKSPACE_IMAGE_INSTRUCTION,
    build_instructions,
)
from omnigent.spec.parser import parse
from omnigent.spec.types import AgentSpec
from omnigent.spec.validator import validate

_SYMBIOSIS_DIR = Path(__file__).resolve().parents[1] / "examples" / "symbiosis"
_EXPECTED_SUBAGENTS = {
    "agy_architect": {
        "model": "gemini-3.8-flash-high",
        "harness": "antigravity-native",
        "skill": "speckit",
    },
    "agy_builder": {
        "model": "gemini-3.8-flash-medium",
        "harness": "antigravity-native",
        "skill": "xerj-code",
    },
    "agy_documenter": {
        "model": "gemini-3.8-flash-low",
        "harness": "antigravity-native",
        "skill": "none",
    },
    "agy_test_engineer": {
        "model": "gemini-3.8-flash-medium",
        "harness": "antigravity-native",
        "skill": "none",
    },
    "claude_adversarial_reviewer": {
        "model": "claude-3-opus",
        "harness": "claude-native",
        "skill": "none",
    },
    "claude_auditor": {
        "model": "claude-3-opus",
        "harness": "claude-native",
        "skill": "none",
    },
    "claude_planner": {
        "model": "claude-3-opus",
        "harness": "claude-native",
        "skill": "none",
    },
    "claude_research": {
        "model": "claude-3-5-haiku",
        "harness": "claude-native",
        "skill": "xerj",
    },
    "claude_surgeon": {
        "model": "claude-3-5-sonnet",
        "harness": "claude-native",
        "skill": "xerj",
    },
    "claude_verifier": {
        "model": "claude-3-5-sonnet",
        "harness": "claude-native",
        "skill": "none",
    },
}


def test_symbiosis_root_agent_spec_load_and_validate() -> None:
    """Symbiosis root orchestrator spec parses and validates cleanly."""
    spec = parse(_SYMBIOSIS_DIR)
    assert isinstance(spec, AgentSpec)
    validate(spec)

    assert spec.name == "symbiosis"
    assert spec.executor is not None
    assert spec.executor.model == "gemini-3.8-flash-high"
    assert spec.executor.config.get("harness") == "antigravity-native"
    assert spec.spawn is True
    assert spec.timers is True

    # Exactly 10 subagents declared in tools.agents
    assert spec.tools is not None
    assert set(spec.tools.agents) == set(_EXPECTED_SUBAGENTS.keys())


def test_symbiosis_all_subagents_spec_load_and_validate() -> None:
    """All 10 Symbiosis subagents load and validate cleanly with expected model tiers."""
    agents_dir = _SYMBIOSIS_DIR / "agents"
    subagent_dirs = [d for d in agents_dir.iterdir() if d.is_dir()]
    assert len(subagent_dirs) == 10

    for subagent_dir in subagent_dirs:
        name = subagent_dir.name
        assert name in _EXPECTED_SUBAGENTS, f"Unexpected subagent directory: {name}"
        expected = _EXPECTED_SUBAGENTS[name]

        sub_spec = parse(subagent_dir)
        assert isinstance(sub_spec, AgentSpec)
        validate(sub_spec)

        assert sub_spec.name == name
        assert sub_spec.executor is not None
        assert sub_spec.executor.model == expected["model"]
        assert sub_spec.executor.config.get("harness") == expected["harness"]

        # Verify whitelisted skills tag in instructions
        allowed_tag = f"[Allowed Skills: {expected['skill']}]"
        assert allowed_tag in (sub_spec.instructions or ""), (
            f"Subagent {name} instructions missing whitelist tag {allowed_tag}"
        )


def test_symbiosis_datamodel_loader() -> None:
    """Symbiosis loads cleanly via datamodel loader (AgentDef) with all 10 AgentTool objects."""
    agent_def = load_agent_def_from_path(str(_SYMBIOSIS_DIR))
    assert isinstance(agent_def, AgentDef)
    assert agent_def.name == "symbiosis"
    assert agent_def.executor == ExecutorSpec(
        model="gemini-3.8-flash-high",
        harness="antigravity-native",
    )

    # 10 subagent tools wired as AgentTool instances
    assert len(agent_def.tools) == 10
    assert set(agent_def.tools.keys()) == set(_EXPECTED_SUBAGENTS.keys())

    for tool_name, tool in agent_def.tools.items():
        assert isinstance(tool, AgentTool)
        assert tool.name == tool_name
        expected = _EXPECTED_SUBAGENTS[tool_name]
        assert tool.executor is not None
        assert tool.executor.model == expected["model"]
        assert tool.executor.harness == expected["harness"]
        assert f"[Allowed Skills: {expected['skill']}]" in (tool.prompt or "")


def test_symbiosis_prompt_composition() -> None:
    """Prompt composition assembles base instructions and framework instructions."""
    spec = parse(_SYMBIOSIS_DIR)
    instructions = build_instructions(spec, None, [])

    # Lead Orchestrator instructions
    assert "Antigravity High (gemini-3.8-flash-high)" in instructions
    assert "Google Antigravity (`agy`)" in instructions
    assert "Anthropic Claude Code (`claude`)" in instructions
    assert "SUBAGENT DISPATCH MECHANISM" in instructions
    assert "sys_session_send" in instructions

    # Sacred Stages and subagents present
    for name in _EXPECTED_SUBAGENTS:
        assert name in instructions
    assert "1. DISCOVERY & CONSTITUTION" in instructions
    assert "2. ADVERSARIAL SDD" in instructions
    assert "3. PLANNING & ALLOCATION" in instructions
    assert "4. BIFURCATED IMPLEMENTATION" in instructions
    assert "5. THREE-TIER ADVERSARIAL VERIFICATION" in instructions
    assert "6. LIVING DOCUMENTATION & MERGE" in instructions

    # Framework instructions injected
    assert SUBAGENT_WAKE_NOTICE_INSTRUCTION in instructions
    assert WORKSPACE_IMAGE_INSTRUCTION in instructions

    # Per-request prompt composition
    per_request = "Focus on fixing module authentication."
    augmented = build_instructions(spec, per_request, [])
    assert per_request in augmented


def test_symbiosis_tool_wiring_with_mock_executor() -> None:
    """MockExecutor executes turn dispatch and receives wired subagent tools."""
    agent_def = load_agent_def_from_path(str(_SYMBIOSIS_DIR))
    tools_list = list(agent_def.tools.values())
    assert len(tools_list) == 10

    ex = MockExecutor()

    # Step 1: Orchestrator delegates task to agy_architect
    ex.enqueue_tool_call(
        "sys_session_send",
        {
            "agent": "agy_architect",
            "title": "draft-spec",
            "args": {"input": "Author spec.draft.md for the new feature."},
        },
    )
    # Step 2: Orchestrator completes turn after receiving subagent response
    ex.enqueue_response("Subagents coordinated successfully across all stages.")

    async def _run_turns():
        # Turn 1: tool dispatch
        events_1 = [e async for e in ex.run_turn([], tools_list, agent_def.prompt or "")]
        assert len(events_1) == 1
        assert isinstance(events_1[0], ToolCallRequest)
        assert events_1[0].name == "sys_session_send"
        assert events_1[0].args["agent"] == "agy_architect"
        assert events_1[0].args["args"]["input"].startswith("Author spec.draft.md")

        # Turn 2: completion
        events_2 = [e async for e in ex.run_turn([], tools_list, agent_def.prompt or "")]
        assert len(events_2) == 1
        assert isinstance(events_2[0], TurnComplete)
        assert events_2[0].response is not None
        assert "coordinated successfully" in events_2[0].response

    asyncio.run(_run_turns())
