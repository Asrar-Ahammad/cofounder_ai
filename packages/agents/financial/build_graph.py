"""LangGraph subgraph compilation for Financial agent."""

from typing import Any

from langgraph.graph import END, START, StateGraph

from packages.agents.financial.model_unit_economics import calculate_unit_economics
from packages.agents.financial.simulate_scenarios import simulate_financial_scenarios
from packages.agents.financial.state import FinancialState
from packages.agents.financial.write_constraints import formulate_constraint_limits


def build_financial_graph() -> Any:
    """Construct and compile the Financial LangGraph execution pipeline.

    Returns:
        CompiledStateGraph: Executable subgraph.
    """
    builder = StateGraph(FinancialState)
    builder.add_node("calculate_unit_economics", calculate_unit_economics)
    builder.add_node("formulate_constraint_limits", formulate_constraint_limits)
    builder.add_node("simulate_scenarios", simulate_financial_scenarios)

    builder.add_edge(START, "calculate_unit_economics")
    builder.add_edge("calculate_unit_economics", "formulate_constraint_limits")
    builder.add_edge("formulate_constraint_limits", "simulate_scenarios")
    builder.add_edge("simulate_scenarios", END)

    return builder.compile()
