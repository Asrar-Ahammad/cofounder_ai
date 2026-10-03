"""Web Agent LangGraph subgraph compiling landing page creation and preview deployment."""

from typing import Any

from langgraph.graph import END, START, StateGraph

from packages.agents.web.deploy_sandbox import deploy_to_sandbox_environment
from packages.agents.web.generate_landing_page import generate_landing_page_html
from packages.agents.web.sanitize_html import sanitize_landing_page_html
from packages.agents.web.screen_web_content import screen_landing_page_compliance
from packages.agents.web.state import WebAgentState


class WebAgent:
    """Specialist agent generating sanitized landing page prototypes and preview deployments."""

    name: str = "web_agent"
    allowed_tools: frozenset[str] = frozenset({"deploy_sandbox_site"})
    consumes: frozenset[str] = frozenset({"landing_page_requested", "venture_validated"})
    emits: frozenset[str] = frozenset({"landing_page_generated", "sandbox_site_deployed"})

    def build_graph(self) -> Any:
        """Construct and compile the Web Agent LangGraph subgraph.

        Returns:
            CompiledStateGraph: Executable landing page builder subgraph.
        """
        builder = StateGraph(WebAgentState)
        builder.add_node("generate_html", generate_landing_page_html)
        builder.add_node("sanitize_html", sanitize_landing_page_html)
        builder.add_node("screen_compliance", screen_landing_page_compliance)
        builder.add_node("deploy_sandbox", deploy_to_sandbox_environment)

        builder.add_edge(START, "generate_html")
        builder.add_edge("generate_html", "sanitize_html")
        builder.add_edge("sanitize_html", "screen_compliance")
        builder.add_edge("screen_compliance", "deploy_sandbox")
        builder.add_edge("deploy_sandbox", END)

        return builder.compile()
