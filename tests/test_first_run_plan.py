"""Tests for _resolve_first_run_plan under different credential scenarios."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest

from omnigent.cli import _resolve_first_run_plan


def _fake_provider_for(*harnesses: str) -> Any:
    """Return a provider lookup that reports only the named harnesses configured."""

    def _lookup(_config: Any, harness: str) -> Any:
        return object() if harness in harnesses else None

    return _lookup


@pytest.fixture(autouse=True)
def _isolate_first_run_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Isolate first-run plan resolution from host environment."""
    monkeypatch.setenv("OMNIGENT_CONFIG_HOME", str(tmp_path))
    monkeypatch.setattr("omnigent.cli_config._promote_global_auth_to_provider", Mock())
    monkeypatch.setattr("omnigent.cli_config._adopt_detected_providers", Mock(return_value=[]))
    # Stub kimi CLI detection so host system state does not affect tests
    monkeypatch.setattr(
        "omnigent.onboarding.harness_install.harness_cli_installed",
        lambda _key: False,
    )


def test_resolve_first_run_plan_no_providers(monkeypatch: pytest.MonkeyPatch) -> None:
    """Scenario 1: No providers configured → prompt interactive configure, return None."""
    configure_interactive = Mock()
    monkeypatch.setattr(
        "omnigent.cli._run_configure_harnesses_interactive",
        configure_interactive,
    )
    monkeypatch.setattr(
        "omnigent.onboarding.provider_config.default_provider_for_harness",
        _fake_provider_for(),
    )

    plan = _resolve_first_run_plan()

    assert plan is None
    configure_interactive.assert_called_once()


def test_resolve_first_run_plan_claude_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    """Scenario 2: Claude-sdk configured → claude-sdk harness with bundled polly agent."""
    configure_interactive = Mock()
    monkeypatch.setattr(
        "omnigent.cli._run_configure_harnesses_interactive",
        configure_interactive,
    )
    monkeypatch.setattr(
        "omnigent.onboarding.provider_config.default_provider_for_harness",
        _fake_provider_for("claude-sdk"),
    )

    plan = _resolve_first_run_plan()

    assert plan is not None
    assert plan.harness == "claude-sdk"
    assert plan.agent is not None
    assert plan.agent.endswith("polly")
    configure_interactive.assert_not_called()


def test_resolve_first_run_plan_antigravity_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    """Scenario 3: Antigravity configured → bundled symbiosis orchestrator agent."""
    configure_interactive = Mock()
    monkeypatch.setattr(
        "omnigent.cli._run_configure_harnesses_interactive",
        configure_interactive,
    )
    monkeypatch.setattr(
        "omnigent.onboarding.provider_config.default_provider_for_harness",
        _fake_provider_for("antigravity"),
    )

    plan = _resolve_first_run_plan()

    assert plan is not None
    assert plan.agent is not None
    assert plan.agent.endswith("symbiosis")
    configure_interactive.assert_not_called()


def test_resolve_first_run_plan_antigravity_takes_priority_over_claude(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Priority verification: When both Antigravity and Claude are configured, Antigravity wins."""
    monkeypatch.setattr(
        "omnigent.cli._run_configure_harnesses_interactive",
        Mock(),
    )
    monkeypatch.setattr(
        "omnigent.onboarding.provider_config.default_provider_for_harness",
        _fake_provider_for("antigravity", "claude-sdk", "codex"),
    )

    plan = _resolve_first_run_plan()

    assert plan is not None
    assert plan.agent is not None
    assert plan.agent.endswith("symbiosis")
