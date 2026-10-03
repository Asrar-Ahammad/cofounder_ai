"""Execution context models for agent runs and tool executions."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AgentInfo:
    """Metadata describing an executing agent."""

    name: str
    allowed_tools: frozenset[str] = field(default_factory=frozenset)
    consumes: frozenset[str] = field(default_factory=frozenset)
    emits: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class AgentContext:
    """Immutable context passed into agent nodes and tool invocations."""

    tenant_id: str
    venture_id: str
    run_id: str
    agent: AgentInfo
    metadata: dict[str, Any] = field(default_factory=dict)
