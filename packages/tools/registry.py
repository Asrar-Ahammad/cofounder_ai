"""Tool registration specifications and registry dictionary."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel


@dataclass(frozen=True)
class ToolSpec:
    """Specification describing a callable tool, its schema, and its requirements."""

    name: str
    description: str
    args_model: type[BaseModel]
    adapter_fn: Callable[..., Any]
    requires_approval: bool = False
    policy_check: Callable[[str, str, BaseModel], None] | None = None


class ToolRegistry:
    """In-memory registry of all available tools across Cofunder."""

    def __init__(self) -> None:
        """Initialize empty tool registry."""
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        """Register a tool specification in the registry.

        Args:
            spec: ToolSpec instance to register.
        """
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec | None:
        """Retrieve a tool specification by name.

        Args:
            name: Unique name of the tool.

        Returns:
            ToolSpec | None: Registered tool spec or None.
        """
        return self._tools.get(name)


tool_registry = ToolRegistry()
