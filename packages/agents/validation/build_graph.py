"""LangGraph subgraph compilation for Validation agent."""

from typing import Any

from langgraph.graph import END, START, StateGraph

from packages.agents.validation.market_sizing import calculate_market_sizing
from packages.agents.validation.scoring.problem_severity import calculate_problem_severity
from packages.agents.validation.scoring.timing_score import calculate_timing_score
from packages.agents.validation.state import ValidationState
from packages.agents.validation.synthesize_report import synthesize_validation_report


def build_validation_graph() -> Any:
    """Construct and compile the Validation LangGraph execution pipeline.

    Returns:
        CompiledStateGraph: Executable subgraph.
    """
    builder = StateGraph(ValidationState)
    builder.add_node("calculate_market_sizing", calculate_market_sizing)
    builder.add_node("calculate_timing_score", calculate_timing_score)
    builder.add_node("calculate_problem_severity", calculate_problem_severity)
    builder.add_node("synthesize_report", synthesize_validation_report)

    builder.add_edge(START, "calculate_market_sizing")
    builder.add_edge("calculate_market_sizing", "calculate_timing_score")
    builder.add_edge("calculate_timing_score", "calculate_problem_severity")
    builder.add_edge("calculate_problem_severity", "synthesize_report")
    builder.add_edge("synthesize_report", END)

    return builder.compile()
